import re
import requests
from FWEB.Futils import Regex as Re
from FWEB.rsLogger import Log
Log = Log("FWEB.Futils.URL")

"""
    -> URL HANDLING
-> One period vs Two Periods?
    - The idea is all URLs have either 1 or 2 periods in the string.
        1. "verge.com"
        2. "www.verge.com"
        - Outside of this, there are only slashes. No more periods.
    - We figure out which it is in the current url
        - if 1 period, sitename is before last period.
        - if 2 periods, sitename is inbetween two periods.
    - We then parse the url to find the base site name.
"""
def get_site_name(url):
    """ -> PUBLIC -> Extract Base Site Name from URL <- """
    if verifyTwoPeriods(url):
        return extract_siteName_two_periods(url)
    return extract_siteName_one_period(url)

# -> get_site_name HELPER for verifying URL has one or two periods.
def verifyTwoPeriods(url: str):
    """ PRIVATE """
    count = 0
    for char in url:
        if char == '.':
            count += 1
    if count >= 2:
        return True
    return False

# -> get_site_name HELPER for urls with one period.
def extract_siteName_one_period(url):
    """ PRIVATE """
    i = 0
    slash_count = 0
    removal_index = 0
    for char in url:
        if char == "/":
            slash_count += 1
            if slash_count == 2:
                removal_index = i+1
        if char == '.':
            return url[removal_index:i]
        i += 1
    return url

# -> get_site_name HELPER for urls with two periods.
def extract_siteName_two_periods(url):
    """ PRIVATE """
    temp = ""
    start = 0
    end = 0
    i = 0
    periodCount = 0
    lastChar = ''
    # -> Part 1
    for char in url:
        if char == '/' and lastChar == '/':
            start = i+1
        if char == '.':
            periodCount += 1
            if periodCount == 2:
                end = i
        if end > 0:
            temp = url[start:end]
            break
        lastChar = char
        i += 1
    # -> Part 2
    n = 0
    match = ""
    for c in temp:
        if c == '.':
            match = temp[n+1:]
        n += 1
    return match

def extract_data_src_url(content: str):
    """ EXPERIMENTAL (under development still) """
    new = content.split("https://")
    for item in new:
        test = Re.contains(":", item)
        if test:
            continue
        if len(item) < 5:
            continue
        return "https://" + item
    return False

def is_valid_url(url):
    """ PUBLIC """
    try:
        response = requests.get(url)
        if response:
            Log.d("URL is valid and exists on the internet")
            return True
    except requests.ConnectionError as e:
        Log.e("URL does not exist on Internet", error=e)
        return False

# if __name__ == '__main__':
#     test = "https://wwwflickeringmythc3c8f7.zapwp.com/q:i/r:0/wp:1/w:1/u:https://cdn.flickeringmyth.com/wp-content/uploads/2021/08/lion-king-600x337.jpg"
#     test1 = extract_data_src_url(test)
#     test2 = is_valid_url(test1)
#     print(test1)


def is_url(content: str):
    """ PUBLIC """
    try:
        if type(content) in [list, tuple]:
            for itemContent in content:
                match = re.search(r'http.?://.*/', add_http(itemContent))
                if match is not None:
                    return True, match.string
            return False, False
        else:
            match = re.search(r'http.?://.*/', add_http(content))
            return True, match.string if match is not None else False
    except Exception as e:
        Log.e(f"Failed to regex findall. {content}", error=e)
        return False, False

def add_http(content):
    if content.startswith("//") or not content.startswith("http"):
        url1 = "https:" + content
        return url1
    return content

def avoid_url(url, avoid_list):
    """ EXPERIMENTAL """
    one = url.replace("https", "")
    two = one.replace("www", "")
    three = two.replace(".", "/")
    final = three.split("/")
    for avoid in avoid_list:
        if avoid in final:
            return True
    return False