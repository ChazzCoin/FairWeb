from newspaper import Article
from FW.JParser import JsonParser
from FNLP import URL
from F.LOG import Log
Log = Log("FairWEB.newspaper3k.ArticleDownloader")

def download_article(url):
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
        article.nlp()
        Log.s(f"Successfully Downloaded Article. Attempting to Parse into Hookup.")
        # -> Parse from Article Object into Hookup Object
        json = JsonParser.parse(article, client="newspaper3k", extractDate=True)
        json["source"] = URL.get_site_name(url)
        return json
    except Exception as e:
        Log.e("Failed to Download Article.", error=e)
        return False

def download_html(url) -> bool:
    """
    - Attempts to download HTML/URL
    - Converts/Returns obj to HookupObj
    - Optional ability to validate hookupObj before returning.
    """
    article = Article(url)
    try:
        # -> Download HTML from URL
        article.download()
        html = article.html
        Log.s(f"Successfully Downloaded Article. Attempting to Parse into Hookup.")
        if html:
            return html
        return False
    except Exception as e:
        Log.e("Failed to Download Article.", error=e)
        return False

def parse_html(url, html):
    article = Article(url)
    article.html = html
    article.parse()
    article.nlp()
    # -> Parse from Article Object into Hookup Object
    json = JsonParser.parse(article, client="newspaper3k", extractDate=True)
    json["source"] = URL.get_site_name(url)
    return json

if __name__ == '__main__':
    url1 = "https://cointelegraph.com/news/price-analysis-1-28-btc-eth-bnb-ada-sol-xrp-luna-doge-dot-avax"
    url2 = "https://www.forbes.com/sites/investor/2022/01/28/ethereum-cardano-polygon-solana-avalanche-and-polkadot-deathmatch-who-wins-who-dies/?sh=4292a4897c9b"
    url3 = "https://www.businessinsider.com/tomi-lahren-spoke-at-police-training-event-dismissed-reform-wapo-2022-1"
    url4 = "https://www.foxbusiness.com/business-leaders/elon-musk-offers-support-to-canadian-truckers-amid-covid-vaccine-mandate"
    newTest2 = "https://towardsdatascience.com/a-step-by-step-guide-to-scheduling-tasks-for-your-data-science-project-d7df4531fc41"
    miner1 = "https://minergate.com/blog"
    download_article(url1)
    # download_html(miner1)