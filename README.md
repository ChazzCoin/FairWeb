# FWEB
FairWeb or FWEB is a complete webpage downloader and web-scrapping tool-kit.

1. FusedDownloader -> Uses two libraries to attempt to download the URL. 
    - v1 = NewsPaper.Article
    - v2 = FWEB.ArchiveDownloader_v1

USAGED:
-> FusedDownloader.download_v2(url)


2. StartCrawler -> Takes a URL and begins to "crawl" the website, downloading and saving every webpage it can.
    - Under the hood, it uses FusedDownloader to actually download and parse the webpage.

3. Core.Tag -> Master Util Library for searching and finding anything inside the returned HTML.
