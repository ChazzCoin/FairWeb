from Crawler.ArchiveCrawler_v2 import ArchiveCrawler
from FWEB import URL, Log

Log = Log("FWEB.StartCrawler")

url = input(" Please enter a URL to Crawl... ")
UrlIsValid = URL.is_valid_url(url)

if UrlIsValid:
    Log.i("Url is Valid. Starting up Archive Crawler...")
    ArchiveCrawler(url)
    Log.i("Crawler is finished!")
