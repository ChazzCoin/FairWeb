from FW.Crawler.Crawl import ArchiveCrawler

DEFAULT_MAX_QUEUE = 500

def run_ListMode(url, maxQueue=DEFAULT_MAX_QUEUE):
    c = ArchiveCrawler.start_SuicideMode(_url=url, max=maxQueue, saveToDB=False)
    return c

def run_suicideMode(url, maxQueue=DEFAULT_MAX_QUEUE):
    c = ArchiveCrawler.start_SuicideMode(_url=url, max=maxQueue)
    return c

def run_unlimitedMode(url, maxQueue=DEFAULT_MAX_QUEUE):
    c = ArchiveCrawler.start_UnlimitedMode(_url=url, maxQueue=maxQueue)
    return c

if __name__ == '__main__':
    url = "https://web.archive.org/web/20130921072250/http://www.bloomberg.com/technology/"
    url2 = "https://web.archive.org/web/20131021173221/http://www.buzzfeed.com/"
    url3 = "https://www.nbcnews.com/"
    url_medium = "https://medium.com/"
    medium = "https://medium.com/"
    science = "https://www.science.org/"
    coindesk = 'https://www.coindesk.com/'
    cryptnews = "https://cryptonews.com/"
    coinbase = "https://blog.coinbase.com/"
    tokenEconomy = "https://tokeneconomy.co/archive"
    bbc = "https://www.bbc.com/"
    guardian = "https://www.theguardian.com/world/2022/jan/26/biden-threatens-putin-with-personal-sanctions-if-russia-invades-ukraine"
    marketwatch = "https://www.marketwatch.com/"
    imdb = "https://www.imdb.com/title/tt0110357/news?ref_=tt_ql_sm"
    cnet = "https://www.cnet.com/news/"
    verge = "https://www.theverge.com/tech"
    yahoo = "https://finance.yahoo.com/"
    engadget = "https://www.engadget.com/"
    meta1 = "https://www.investors.com"
    meta2 = "https://www.minergate.com/blog"
    meta3 = "https://www.pocketgamer.biz"
    meta4 = "https://www.uktech.news"
    meta5 = "https://www.newsanyway.com"
    meta6 = "https://cointelegraph.com/tags/nft"
    meta7 = "https://cryptoslate.com/defi/"
    meta8 = "https://medium.com/tag/machine-learning"
    meta9 = "https://www.barrons.com/topics/technology?mod=BOL_TOPNAV"
    meta10 = "http://www.coinnewsasia.com/"
    # if guard in guardian:
    #     print(True)
    run_suicideMode(meta10)