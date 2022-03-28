urls = [
    "https://www.americanbanker.com/payments/news/inside-ripples-plans-for-mainstream-crypto-payments",
    "https://blockworks.co/new-crypto-venture-capital-fund-investing-only-in-near-in-nod-to-specialization/",
    "https://towardsdatascience.com/a-step-by-step-guide-to-scheduling-tasks-for-your-data-science-project-d7df4531fc41",
    "https://blog.feedspot.com/technology_rss_feeds/",
    "https://libguides.wlu.edu/c.php?g=357505&p=2412837",
    "https://www.facebook.com/events/614844569594632",
    "https://web.archive.org/web/20131005150341/http://topics.bloomberg.com/bloomberg-pursuits/",
    "https://en.wikipedia.org/wiki/IMDb",
    "https://www.flickeringmyth.com/2021/08/aaron-pierre-and-kelvin-harrison-jr-will-voice-mufasa-and-scar-in-barry-jenkins-the-lion-king-prequel/",
    "https://www.goldderby.com/article/2021/barry-jenkins-lion-king-prequel-mufasa-scar/",
    "https://www.cbsnews.com/news/stephen-breyer-supreme-court-justice-retiring-biden-pick/",
    "https://www.cnn.com/2022/01/26/europe/ukraine-russia-normandy-format-ceasefire-talks-intl-hnk/index.html",
    "https://www.nytimes.com/2022/01/26/business/media/cnn-plus-streaming-news.html",
    "https://hackaday.com/2022/01/26/turn-on-sarcasm-with-the-flip-of-a-switch/",
    "https://news.yahoo.com/secret-button-iphones-big-hit-213305165.html",
    "https://news.yahoo.com/navy-seals-stop-using-washington-014909586.html",
    "https://www.bbc.com/news/world-europe-60145159",
    "https://medium.com/the-node-js-collection/understanding-measuring-http-timings-with-node-js-c315fbbf70f4",
    "https://www.reddit.com/r/FlareNetworks/",
    "https://www.reddit.com/r/FlareNetworks/comments/ru1tlo/the_flare_community_is_seeing_an_increase_in/",
    "https://opensea.io/blog/announcements/opensea-acquires-dharma-labs-welcomes-new-cto/",
    "https://www.reddit.com/r/whatsthisbug/comments/sepqer/before_we_enjoy_the_rest_of_the_blackberries/",
    "https://www.bbc.com/news/world-europe-60145159",
    "https://www.theguardian.com/us-news/live/2022/mar/01/joe-biden-state-of-the-union-address-putin-russia-ukraine-live-latest"
]

both_success = []
both_failed = []
v1_wins = []
v2_wins = []


def compare(url, json_v1, json_v2):
    from Utils import DICT
    val_v1 = False
    date_v1 = DICT.get("published_date", json_v1)
    body_v1 = DICT.get("body", json_v1)
    val_v2 = False
    date_v2 = DICT.get("date", json_v2)
    body_v2 = DICT.get("body", json_v2)

    if date_v1 and not body_v1.startswith("Something went wrong"):
        val_v1 = True
    if date_v2 and not body_v2.startswith("Something went wrong"):
        val_v2 = True
    if val_v1 and val_v2:
        both_success.append(url)
    elif val_v1 and not val_v2:
        v1_wins.append(url)
    elif val_v2 and not val_v1:
        v2_wins.append(url)
    else:
        both_failed.append(url)

from FWEB.Downloader.ArchiveDownloader_v1 import DownloadWebPage
from FWEB.Downloader import ArticleDownloader
from FWEB import FusedDownloader

def test1():
    for url in urls:
        downloader_v1 = ArticleDownloader.download_article(url)
        downloader_v2 = DownloadWebPage.start_url(url).json
        compare(url, downloader_v1, downloader_v2)

def test2():
    for url in urls:
        FusedDownloader.download_v2(url)

test1()

print("Total Urls Tried:", len(urls))
print("Both Success:", len(both_success))
print("Both Failed:", len(both_failed))
print("v1 Only:", len(v1_wins))
print("v2 Only:", len(v2_wins))

