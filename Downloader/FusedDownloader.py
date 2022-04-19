from Downloader.ArchiveDownloader_v1 import DownloadWebPage
from Downloader import ArticleDownloader
from fwebCore import Validator
from fwebUtils.LOGGER import Log
Log = Log("FWEB.FusedDownloader")

updateUrl = False

@Validator.download_save
def download(url):
    if not url:
        Log.e(f"Url argument is invalid.")
        return False
    # -> v1
    downloader_v1 = fweb_downloader_v1(url)
    if downloader_v1:
        json_v1 = Validator.validate_article(downloader_v1)
        if json_v1:
            return downloader_v1
    # -> v2
    Log.i(f"Downloading Article from CLIENT=[ User ]")
    downloader_v2 = fweb_downloader_v2(url, client="User")
    if downloader_v2:
        json_v2 = Validator.validate_article(downloader_v2)
        if json_v2:
            return downloader_v2.json
    return False


# def updateUrlStatus(url, status):
#     if updateUrl:
#         if status == "success":
#             return dbURL.UPDATE_TO_SUCCESS(url)
#         return dbURL.UPDATE_TO_FAILED(url)
#     return False

@Validator.mongo_save
def crawler_downloader(url, response):
    # -> v2
    downloader_v2 = fweb_response(url, response, client="archive crawler")
    if downloader_v2 and Validator.validate_article(downloader_v2):
        # updateUrlStatus(url, "success")
        return downloader_v2.json
    # -> v1
    downloader_v1 = fweb_downloader_v1(url)
    if downloader_v1 and Validator.validate_article(downloader_v1):
        # updateUrlStatus(url, "success")
        return downloader_v1
    # updateUrlStatus(url, "failed")
    return False

@Validator.mongo_save
def client_downloader(url, client):
    if not url:
        Log.e(f"Url argument is invalid.")
        return False
    # -> v1
    downloader_v1 = fweb_downloader_v1(url)
    if downloader_v1:
        json_v1 = Validator.validate_article(downloader_v1)
        if json_v1:
            # updateUrlStatus(url, "success")
            return downloader_v1
    # -> v2
    Log.i(f"Downloading Article from CLIENT=[ {client} ]")
    downloader_v2 = fweb_downloader_v2(url, client=client)
    if downloader_v2:
        json_v2 = Validator.validate_article(downloader_v2)
        if json_v2:
            # updateUrlStatus(url, "success")
            return downloader_v2.json
    # updateUrlStatus(url, "failed")
    return False

def fweb_downloader_v1(url):
    return ArticleDownloader.download_article(url)

def fweb_downloader_v2(url, client="fweb_downloader_v2"):
    extractor = DownloadWebPage.start_url(url, client=client)
    return extractor

def fweb_response(url, response, client="fweb_response"):
    extractor = DownloadWebPage.start_response(url, response, client=client)
    return extractor