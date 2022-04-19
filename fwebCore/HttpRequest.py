import requests
from fwebUtils import Ext
from fwebUtils.LOGGER import Log
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
    "path": "/",
    "authorization": "Bearer -aojfsjQQfzLu5OQhdrIGa3-nNcdOcw",
    "method": "GET",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
    "accept-language": "en-US,en;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "content-type": "text/html; application/json",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "referer": "https://www.birminghamunited.com/",
    "sec-fetch-mode": "navigate",
    "sec-ch-ua": "'Not A;Brand';v='99', 'Chromium';v='99', 'Google Chrome';v='99'",
    "x-reddit-loid": "0000000000jbyluro4.2.1643937203173.Z0FBQUFBQmhfSDJ6NGQyeklHbnktQ1Eyc3hzWnRmVVlsUkp3V0dNaWliUkZwWkxKeGhRYTZIUEI4aEVCN1lwOHVrcGhLenJUUjJHR3RoaEJJNUtxZEFiS0xHLUxITFdhc3JWSmtidFA2bl9JMEJBU2t0OERrVWJuWmQ0eFdfbjVIX0lOSEpBakdZaVg",
    "x-reddit-session": "fjdalplnjkjbolfahk.0.1648588049034.Z0FBQUFBQmlRM1VSYm56T2EyckhKTV9qQ0RULWRrX25RMUpnSjU5MTBWYzFDVEd2b0lvZXh0OVlCVnRXQk5KVGNzbzlGR3g3Z0hTR3VHXzVsazhwSFkyZkpxdkhnNGl3RGNuM1VwZXlVYmNqX0R0RjRkbHkySlBhbW1hQXowUm5qRWtLLTV0clNpLXU"
}
COOKIES = {'from-my': 'browser'}

PROXIES = {
  'http': 'http://10.10.1.10:3128',
  'https': 'http://10.10.1.10:1080',
}


# -> Step One -> Call URL and get Raw HTML back in Response Object.
# @Ext.safe_run
@Ext.sleep(5)
def get_request(url):
    # HEADERS["user-agent"] = Resources.get_random_user_agent()
    Log.i("Making HTTP Request.", v=f"URL= [ {url} ] ")
    response = requests.get(url, headers=HEADERS_EXT)
    if response.status_code > 205:
        Log.w(f"Failed to make HTTP Request with URL= [ {url} ] ")
        return False
    else:
        Log.s(f"Successful HTTP Request")
        return True, response
