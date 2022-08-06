from FW.Core.CoreDownloaders.ArchiveDownloader_v1 import DownloadWebPage
from FW.Core.CoreDownloaders import ArticleDownloader
from FW.Core import Validator
from F import EXT
from F.LOG import Log
Log = Log("FairWEB.FusedDownloader")

from F.CLASS import Thread

@EXT.safe_run
def download_v1(url, saveToArchive=False, setDateToToday=False):
    # -> v1
    downloader_v1 = fweb_downloader_v1(url)
    if downloader_v1:
        result = Validator.validateAndSave(saveToArchive, setDateToToday, downloader_v1)
        return result
    # -> v2
    downloader_v2 = fweb_downloader_v2(url).json
    if downloader_v2:
        result = Validator.validateAndSave(saveToArchive, setDateToToday, downloader_v2)
        return result
    return False

# def download(url):
#     return download_v2(url)

def downloadCallback(result):
    print(result)
    return result

@Validator.mongo_save
def download_v2(url):
    # -> v1
    downloader_v1 = fweb_downloader_v1(url)
    if downloader_v1 and Validator.validate_article(downloader_v1):
        return downloader_v1
    # -> v2
    # downloader_v2 = fweb_downloader_v2(url)
    # if downloader_v2 and Validator.validate_article(downloader_v2):
    #     return downloader_v2.json
    return False

def download(url):
    # -> v1
    downloader_v1 = fweb_downloader_v1(url)
    return downloader_v1 if downloader_v1 else False

@Thread.runInBackground()
def downloadInBackground(url):
    # -> v1
    downloader_v1 = fweb_downloader_v1(url)
    return downloader_v1 if downloader_v1 else False

@Validator.mongo_save
def crawler_downloader(url, response):
    # -> v2
    downloader_v2 = fweb_response(url, response, client="archive crawler")
    if downloader_v2 and Validator.validate_article(downloader_v2):
        return downloader_v2.json
    # -> v1
    downloader_v1 = fweb_downloader_v1(url)
    if downloader_v1 and Validator.validate_article(downloader_v1):
        return downloader_v1
    return False

@Validator.mongo_save
def client_downloader(url, client):
    if not url:
        Log.e(f"Url argument is invalid.")
        return False
    # -> v1
    Log.i(f"1. Attempting newspaper3k Download of Article from CLIENT=[ {client} ]")
    downloader_v1 = fweb_downloader_v1(url)
    if downloader_v1:
        json_v1 = Validator.validate_article(downloader_v1)
        if json_v1:
            return downloader_v1
    # -> v2
    Log.i(f"2. Attempting FairDownloader Download of Article from CLIENT=[ {client} ]")
    downloader_v2 = fweb_downloader_v2(url, client=client)
    if downloader_v2:
        json_v2 = Validator.validate_article(downloader_v2)
        if json_v2:
            return downloader_v2.json
    return False

def fweb_downloader_v1(url):
    """ Original Article Downloader -> newspaper3k """
    return ArticleDownloader.download_article(url)

def fweb_downloader_v2(url, client="fweb_downloader_v2"):
    """ Fair Article Downloader -> URL Based """
    extractor = DownloadWebPage.start_url(url, client=client)
    return extractor

def fweb_response(url, response, client="fweb_response"):
    """ Fair Article Downloader -> HTTP Response Based """
    extractor = DownloadWebPage.start_response(url, response, client=client)
    return extractor

if __name__ == '__main__':
    url1 = "https://www.americanbanker.com/payments/news/inside-ripples-plans-for-mainstream-crypto-payments",
    url2 = "https://towardsdatascience.com/decorators-in-python-fundamentals-for-data-scientists-eada7f4eba85"
    url3 = "https://www.wsj.com/articles/meta-platforms-facebook-fb-q1-earnings-report-2022-1165102219"
    url4 = "https://www.newsobserver.com/news/business/article260136540.html"
    wallstreetj = "https://www.wsj.com/articles/primary-elections-2022-south-carolina-nevada-races-test-trumps-sway-in-gop-11655199002"
    date_none = "https://finance.yahoo.com/news/metaverse-real-estate-market-growing-115600231.html"
    url5 = "https://www.reuters.com/business/media-telecom/jury-alex-jones-defamation-case-begin-deliberations-punitive-damages-2022-08-05/"
    t = downloadInBackground(url5)
    # t = download_v2(date_none)