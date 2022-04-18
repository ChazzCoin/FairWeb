from newspaper import Article
from fwebParser import JsonParser
from fwebLogger.LOGGER import Log
Log = Log("FWEB.Downloader.ArticleDownloader")

def download_article(url) -> bool:
    """
    - Attempts to download HTML/URL
    - Converts/Returns obj to HookupObj
    - Optional ability to validate hookupObj before returning.
    """
    article = Article(url)
    try:
        # -> Download HTML from URL
        article.download()
        # -> Initial Parsing from HTML to Article Object
        article.parse()
        Log.s(f"Successfully Downloaded Article. Attempting to Parse into Hookup.")
        # -> Parse from Article Object into Hookup Object
        json = JsonParser.parse(article, client="article downloader")
        return json
    except Exception as e:
        Log.e("Failed to Download Article.", error=e)
        return False

# if __name__ == '__main__':
#     url1 = "https://cointelegraph.com/news/price-analysis-1-28-btc-eth-bnb-ada-sol-xrp-luna-doge-dot-avax"
#     url2 = "https://www.forbes.com/sites/investor/2022/01/28/ethereum-cardano-polygon-solana-avalanche-and-polkadot-deathmatch-who-wins-who-dies/?sh=4292a4897c9b"
#     url3 = "https://www.businessinsider.com/tomi-lahren-spoke-at-police-training-event-dismissed-reform-wapo-2022-1"
#     url4 = "https://www.foxbusiness.com/business-leaders/elon-musk-offers-support-to-canadian-truckers-amid-covid-vaccine-mandate"
#     newTest2 = "https://towardsdatascience.com/a-step-by-step-guide-to-scheduling-tasks-for-your-data-science-project-d7df4531fc41"
#     download_article(url1)