from FW.FusedDownloader import FusedDownloader
from F.LOG import Log
from FCM.Jarticle.jProvider import jPro
Log = Log("FWEB.Crawler.ArchiveCrawler_v2")

jpro = jPro()




# -> 2. Download Article
def attempt_download(url, saveToDB=True, strictMode=False):
    Log.i("Attempting Archive Download.")
    if strictMode and jpro.article_url_exists(url):
        print("Article URL Already exists in DB.")
        return
    if saveToDB:
        return FusedDownloader.download_v2(url)
    else:
        return FusedDownloader.download(url)