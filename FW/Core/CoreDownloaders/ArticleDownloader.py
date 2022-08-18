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
