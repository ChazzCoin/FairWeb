from FWEB.Downloader.ArchiveDownloader_v1 import DownloadWebPage
from FWEB.Downloader import ArticleDownloader
from FWEB.Core import Validator
from FWEB.Futils import Ext
from FWEB.rsLogger import Log
Log = Log("FWEB.FusedDownloader")

@Ext.safe_run
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

@Validator.mongo_save
def download_v2(url):
    # -> v1
    downloader_v1 = fweb_downloader_v1(url)
    if downloader_v1 and Validator.validate_article(downloader_v1):
        return downloader_v1
    # -> v2
    downloader_v2 = fweb_downloader_v2(url)
    if downloader_v2 and Validator.validate_article(downloader_v2):
        return downloader_v2.json
    return False

# @Ext.safe_run_return(False)
def fweb_downloader_v1(url):
    return ArticleDownloader.download_article(url)

# @Ext.safe_run_return(False)
def fweb_downloader_v2(url):
    extractor = DownloadWebPage.start_url(url)
    return extractor

if __name__ == '__main__':
    url1 = "https://www.americanbanker.com/payments/news/inside-ripples-plans-for-mainstream-crypto-payments",
    url2 = "https://towardsdatascience.com/decorators-in-python-fundamentals-for-data-scientists-eada7f4eba85"
    fweb_downloader_v1(url2)