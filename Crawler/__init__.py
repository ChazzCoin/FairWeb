from Jarticle.jURL import jURL
from Crawler.ArchiveCrawler_v2 import ArchiveCrawler
from fwebUtils import URL, Regex
from fwebUtils.LOGGER import Log
Log = Log("FWEB.StartCrawler")

# todo: fix this jURL!
def runDbUrls():
    Log.i("Running Crawl on Database URL Queue...")
    u = jURL().url_constructor()
    _urls = u.get_urls("000")
    for single_url in _urls:
        try:
            crawl_url(single_url)
        except Exception as e:
            Log.e(f"Failed to crawl URL= [ {single_url} ]", error=e)
            continue

def runSingleUrl(_url):
    Log.i(f"Running Crawl on URL= [ {_url} ] ...")
    UrlIsValid = URL.is_valid_url(_url)
    if UrlIsValid:
        crawl_url(_url)

def crawl_url(_url):
    Log.i("Starting up Archive Crawler...")
    ArchiveCrawler.start_SuicideMode(_url, max=200)
    Log.i("Crawler is finished!")

def init(user_input=None):
    if not user_input:
        user_input = input(" Please enter a URL to Crawl... ")
    if Regex.contains("database", user_input):
        runDbUrls()
    else:
        runSingleUrl(user_input)