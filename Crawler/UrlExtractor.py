from Core import HttpRequest, Soup
from FLog.LOGGER import Log
Log = Log("FairWEB.Crawler.UrlExtractor")

def request_and_parse(_url):
    try:
        # Log.v("Making Request via requests and parsing html via bs4.")
        response = HttpRequest.get_request(_url)
        return Soup.to_html(response)
    except Exception as e:
        Log.e("Failed to make request.", error=e)

def extract_urls(url):
    Log.v("Extracting URLs via Soup.")
    return request_and_parse(url).findAll('a', href=True)