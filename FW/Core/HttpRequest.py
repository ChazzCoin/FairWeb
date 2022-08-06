import time

import requests
from FW.Core import Soup
from http.cookiejar import CookieJar as cj
from FW.Core.CoreDownloaders import ArticleDownloader
from F import LIST

import FairResources
from F import EXT
from F.LOG import Log
Log = Log("FWEB.Core.HttpRequest")

FAIL_ENCODING = 'ISO-8859-1'

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
    ":authority": "sec.report",
    ":scheme": "https",
    ":method": "GET",
    ":path": "/CIK/Search/Lockheed+Martin+Corporation+Common+Stock",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
    "accept-language": "en-US,en;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "content-type": "text/html",
    "accept": "application/signed-exchange;v=b3;q=0.7,*/*;q=0.8",
    "referer": "https://sec.report/Senate-Stock-Disclosures",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-dest": "empty",
    "sec-fetch-site": "same-origin",
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
@EXT.sleep(1)
def get_request(url):
    try:
        HEADERS["user-agent"] = FairResources.get_random_user_agent()
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

def get_request_3k_to_html(url, parseToSoup=True):
    time.sleep(1)
    try:
        Log.v("Making Request via requests and parsing html via bs4.")
        html = ArticleDownloader.download_html(url)
        Log.v("Request Made.")
        if parseToSoup:
            Log.v("Parsing into Soup Object.")
            parsed_html = Soup.Parse(rawText=html)
            return parsed_html
        return html
    except Exception as e:
        Log.e(f"Failed to get HTML from URL=[ {url} ]", error=e)
        return False

@EXT.sleep(1)
def get_request_v2(url):
    try:
        HEADERS["user-agent"] = FairResources.get_random_user_agent()
        Log.i("Making HTTP Request.", v=f"URL= [ {url} ] ")
        response = requests.get(url, **get_request_kwargs())
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

# -> Step One -> Call URL and get Raw HTML back in Response Object.
def request_to_html_v2(url):
    Log.i(f"Making Request to URL = [ {url} ]")
    resp = get_request_v2(url)
    if resp:
        response = LIST.get(1, resp, False)
        return to_html_v2(response)
    return False

def to_html_v2(response):
    if response.encoding != FAIL_ENCODING:
        # return response as a unicode string
        html = response.text
    else:
        html = response.content
        if 'charset' not in response.headers.get('content-type'):
            encodings = response.utils.get_encodings_from_headers(response.headers)
            if len(encodings) > 0:
                response.encoding = encodings[0]
                html = response.text
    return html or ''

def get_request_kwargs():
    """This Wrapper method exists b/c some values in req_kwargs dict
    are methods which need to be called every time we make a request
    """
    HEADERS["user-agent"] = FairResources.get_random_user_agent()
    timeout = 7
    proxies = {}
    return {
        'headers': HEADERS,
        'cookies': cj(),
        'timeout': timeout,
        'allow_redirects': True,
        'proxies': proxies
    }

if __name__ == '__main__':
    from Soup import BeautifulSoup
    from bs4.dammit import EncodingDetector
    url1 = "https://cointelegraph.com/news/price-analysis-1-28-btc-eth-bnb-ada-sol-xrp-luna-doge-dot-avax"
    date_none = "https://finance.yahoo.com/news/metaverse-real-estate-market-growing-115600231.html"
    tableUrl = "https://www.quiverquant.com/dashboard/NVDA/"
    table2 = "https://sec.report/Senate-Stock-Disclosures"
    test = get_request_v2(table2)
    test2 = get_request(table2)
    resp = LIST.get(1, test)
    resp2 = LIST.get(1, test2)
    http_encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
    html_encoding = EncodingDetector.find_declared_encoding(resp.content, is_html=True)
    encoding = html_encoding or http_encoding
    testing = BeautifulSoup(resp.text, 'lxml', from_encoding=encoding)
    resp = str(resp.text)
    print(resp)
    arttt = ArticleDownloader.parse_html(date_none, resp)
    print(arttt)