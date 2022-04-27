from Crawler.ArchiveCrawler_v2 import ArchiveCrawler
from fairNLP import URL, Regex
from FLog.LOGGER import Log
Log = Log("FairWEB.StartCrawler")

def runDbUrls(_urls):
    Log.i("Running Crawl on Database URL Queue...")
    for single_url in _urls:
        try:
            crawl(single_url)
        except Exception as e:
            Log.e(f"Failed to crawl URL= [ {single_url} ]", error=e)
            continue

def runSingleUrl(_url):
    Log.i(f"Running Crawl on URL= [ {_url} ] ...")
    UrlIsValid = URL.is_valid_url(_url)
    if UrlIsValid:
        crawl(_url)

def crawl(_url):
    Log.i("Starting up Archive Crawler...")
    ArchiveCrawler.start_SuicideMode(_url, max=200)
    # ArchiveCrawler(_url, max=200, suicideMode=True).run()
    Log.i("Crawler is finished!")

def init(user_input=None):
    if not user_input:
        user_input = input(" Please enter a URL to Crawl... ")
    if Regex.contains("database", user_input):
        runDbUrls()
    else:
        runSingleUrl(user_input)
