from FWEB.Downloader.ArchiveDownloader_v1 import Extract
from FWEB.Downloader import ArticleDownloader
from FWEB import Validator, Ext, Log
Log = Log("FWEB.FusedDownloader")

@Ext.safe_run
@Ext.sleep(5)
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

@Ext.sleep(5)
@Validator.mongo_save
def download_v2(url):
    # -> v1
    downloader_v1 = fweb_downloader_v1(url)
    if downloader_v1 and Validator.validate_article(downloader_v1):
        return downloader_v1
    # -> v2
    downloader_v2 = fweb_downloader_v2(url).json
    if downloader_v2 and Validator.validate_article(downloader_v2):
        return downloader_v2
    return False

def fweb_downloader_v1(url):
    return ArticleDownloader.download_article(url)

def fweb_downloader_v2(url):
    return Extract().start_url(url)

# if __name__ == '__main__':
#     url1 = "https://www.americanbanker.com/payments/news/inside-ripples-plans-for-mainstream-crypto-payments",
#     url2 = "https://towardsdatascience.com/decorators-in-python-fundamentals-for-data-scientists-eada7f4eba85"
#     download_v2(url2)