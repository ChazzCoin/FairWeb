from . import FusedDownloader
from .Crawler.ArchiveCrawler_v2 import ArchiveCrawler
from .Downloader import ArchiveDownloader_v1
from .Downloader import ArticleDownloader
from .fwebCore import Tag, Validator, Soup, HttpRequest
from .fwebLogger.LOGGER import Log
from .FQueue.UrlQueue import FQueue
from .fwebUtils import Ext, Regex, URL, DICT, DATE, LIST, Language

__version__ = "1.0.0"
__author__ = 'ChazzCoin'
__credits__ = 'Tiffany Systems'

def downloadWebPage(url):
    return FusedDownloader.download(url)

def crawlWebSite(url):
    return ArchiveCrawler.start_SuicideMode(url)

downloadUrl = lambda url: FusedDownloader.download(url)