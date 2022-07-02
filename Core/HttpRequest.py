import requests
from Core import Soup

from FList import LIST

import Resources
from FExt import EXT
from FLog.LOGGER import Log
Log = Log("FWEB.Core.HttpRequest")

HEADERS = {
    "scheme": "https",
    "method": "GET",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
    "accept-language": "en-US",
    "accept-encoding": "gzip, deflate, br",
    "content-type": "text/html",
    "accept": "text/html",
    "referer": "https://www.google.com/",
}
HEADERS_EXT = {
    "scheme": "https",
    "path": "/public/event/2038/individual-team/18/11332/9",
    "method": "GET",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
    "accept-language": "en-US,en;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "content-type": "text/html",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "referer": "https://www.birminghamunited.com/",
    "sec-fetch-mode": "navigate",
    "sec-fetch-dest": "document",
    "sec-fetch-site": "cross-site",
    "sec-fetch-user": "?1",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "macOS",
    "upgrade-insecure-requests": "1",
    "sec-ch-ua": "'Not A;Brand';v='99', 'Chromium';v='99', 'Google Chrome';v='99'"
}
COOKIES = {'from-my': 'browser'}

PROXIES = {
  'http': 'http://10.10.1.10:3128',
  'https': 'http://10.10.1.10:1080',
}


# -> Step One -> Call URL and get Raw HTML back in Response Object.
# @Ext.safe_run
@EXT.sleep(5)
def get_request(url):
    try:
        HEADERS["user-agent"] = Resources.get_random_user_agent()
        Log.i("Making HTTP Request.", v=f"URL= [ {url} ] ")
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code > 205:
            Log.w(f"Failed to make HTTP Request with URL= [ {url} ] ")
            return False
        else:
            Log.s(f"Successful HTTP Request")
            return True, response
    except Exception as e:
        Log.e("Request Failed.", error=e)
        return False

# -> Step One -> Call URL and get Raw HTML back in Response Object.
def request_to_html(url):
    Log.i(f"Making Request to URL = [ {url} ]")
    resp = get_request(url)
    if resp:
        response = LIST.get(1, resp, False)
        return to_html(response)
    return False

# -> Step Two -> Convert Response Object to HTML Object
def to_html(response):
    try:
        Log.i(f"Parsing Response Text to HTML Objects.")
        return Soup.Parse(response)
    except Exception as e:
        Log.e("Failed to parse into HTML.", error=e)
        return False

if __name__ == '__main__':
    date_none = "https://finance.yahoo.com/news/metaverse-real-estate-market-growing-115600231.html"
    request_to_html(date_none)