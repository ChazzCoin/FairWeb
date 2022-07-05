from FusedDL import FusedDownloader
from FLog.LOGGER import Log
Log = Log("FWEB.Crawler.ArchiveCrawler_v2")


# -> 2. Download Article
def attempt_download(url):
    Log.i("Attempting Archive Download.")
    result = FusedDownloader.download_v2(url)
    if result:
        Log.v("Extraction Success")
        return True
    else:
        Log.v("Extraction Failed")
        return False