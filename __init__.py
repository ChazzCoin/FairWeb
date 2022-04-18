# import FusedDownloader
from Downloader import FusedDownloader
from .Crawler.ArchiveCrawler_v2 import ArchiveCrawler

__version__ = "1.0.0"
__author__ = 'ChazzCoin'
__credits__ = 'Tiffany Systems'

# def downloadWebPage(url):
#     return FusedDownloader.download(url)

def crawlWebSite(url):
    return ArchiveCrawler.start_SuicideMode(url)

# downloadUrl = lambda url: FusedDownloader.download(url)