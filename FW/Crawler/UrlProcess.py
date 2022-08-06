from FW.FusedDownloader import FusedDownloader
from F.LOG import Log
Log = Log("FWEB.Crawler.ArchiveCrawler_v2")


# -> 2. Download Article
def attempt_download(url, saveToDB=True):
    Log.i("Attempting Archive Download.")
    if saveToDB:
        return FusedDownloader.download_v2(url)
    else:
        return FusedDownloader.download(url)