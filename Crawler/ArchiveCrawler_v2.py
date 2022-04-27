import os
from bs4 import BeautifulSoup
from FSON import DICT
from FList import LIST
from fairNLP import URL
from FusedDL import FusedDownloader
from Core import HttpRequest
from FQueue.UrlQueue import FQueue
from FLog.LOGGER import Log
Log = Log("FWEB.Crawler.ArchiveCrawler_v2")

way_back_machine_url = "https://web.archive.org"
avoid_list = ['youtube', 'twitter', 'facebook', 'instagram', 'advertising', 'apple', 'google',
              'spotify', 'tiktok', 'soundcloud', 'linkedin', 'flickr', 'oauth', 'terms-of-service',
              'privacy-policy', 'contact-us', 'fr', 'de', "coupon.", "coupons.", ".coupon", ".coupons"]


class SoupError(Exception):
    def __init__(self, message, errors=None):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        # Now for your custom code...
        self.errors = errors

class KillThySelf(Exception):
    def __init__(self, message, errors=None):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        # Now for your custom code...
        self.errors = errors

class Modes:
    NORMAL = "NORMAL"
    SUICIDE = "SUICIDE"
    KILL = "KILL"

class ArchiveCrawler:
    pid = None
    timer = None
    # -> kwargs
    max = 100
    suicideSwitch = False
    # -> Global
    MODE = Modes.NORMAL
    queue: FQueue = None
    extraction_success = []
    extraction_failed = []
    stay_within = ""
    soup = None
    total_count = 0

    def __init__(self, url, **kwargs):
        """
        -> Takes single URL, grabs every URL, then tries to download them all.
        -> Takes next URL, grabs every URL, tries to download them all.
        -> !Potential for Forever-Loop!
        """
        self.handle_kwargs(**kwargs)
        self.pid = os.getpid()
        self.stay_within = URL.get_site_name(url)
        self.queue = FQueue(maxSize=self.max, avoidList=avoid_list)
        Log.i(f"Launching ArchiveCrawler with PID=[ {self.pid} ]")
        self.queue.add(url)
        Log.i(f"Ready to START: ArchiveCrawler PID=[ {self.pid} ]")

    @classmethod
    def start(cls, _url, **kwargs):
        cls(_url, **kwargs).run()

    @classmethod
    def start_NormalMode(cls, _url, **kwargs):
        kwargs["suicideMode"] = False
        cls(_url, **kwargs).run()

    @classmethod
    def start_SuicideMode(cls, _url, **kwargs):
        kwargs["suicideMode"] = True
        cls(_url, **kwargs).run()

    def handle_kwargs(self, **kwargs):
        self.max = DICT.get("max", kwargs, default=100)
        self.suicideSwitch = DICT.get("suicideMode", kwargs, default=False)

    def run(self):
        Log.i(f"STARTING: ArchiveCrawler PID=[ {self.pid} ]")
        self.run_spider_queue()

    def verify_mode(self):
        if self.MODE == Modes.NORMAL:
            self.suicideCheck()
            return True
        if self.MODE == Modes.SUICIDE:
            return False
        if self.MODE == Modes.KILL:
            # -> If time goes beyond X amount in the future...
            self.killThySelf()

    def change_mode(self, newMode):
        self.MODE = newMode

    def run_spider_queue(self):
        Log.i(f"Starting URL Queue with {self.queue.size()}.")
        # -> Work Queue.
        while not self.queue.isEmpty():
            # -> Clean Queue Check.
            if self.queue.size() > self.max / 2:
                Log.v("Cleaning Queue.")
                self.queue.clean()
            Log.v("Getting next item in Queue.")
            _url = self.queue.get()
            # -> Attempt Download
            self.attempt_download(_url)
            # -> Begin to die? or Continue as Normal?
            if self.verify_mode():
                # -> Run URL Extraction
                self.extract_urls(_url)
            self.print_status()

    def attempt_download(self, url):
        Log.i("Attempting Archive Download.")
        result = FusedDownloader.download_v2(url)
        if result:
            Log.v("Extraction Success")
            self.extraction_success.append(url)
        else:
            Log.v("Extraction Failed")
            self.extraction_failed.append(url)

    def request(self, _url):
        try:
            Log.v("Making Request via requests and parsing html via bs4.")
            request_response = HttpRequest.get_request(_url)
            response = LIST.get(1, request_response)
            self.soup = BeautifulSoup(response.text, 'html.parser')
            Log.v("Request Made")
        except Exception as e:
            Log.e("Failed to make request.", error=e)

    def extract_urls(self, _url):
        # -> Request
        self.request(_url)
        # -> Parse out URLs
        if self.soup is None:
            return False
        Log.v("Extracting URLs via Soup.")
        extracted_urls = self.soup.findAll('a', href=True)
        # -> Add all URLs to Queue
        self.handle_extracted_urls(extracted_urls)

    """
    -> Need to verify that url we are getting isn't just the ext of the base url.
    -> We are missing URLS!!!
    url = www.cnet.com
    ext = '/news/steve-wilhite-creator-of-the-gif-dies/'
    """
    def handle_extracted_urls(self, extracted_urls):
        if not extracted_urls:
            Log.i("No Extracted URLS")
            return
        Log.i("Looping extracted urls.")
        for item in extracted_urls:
            if self.queue.isFull():
                Log.i("Queue is FULL!")
                return
            _url = DICT.get("href", item)
            Log.d(f"Looking at URL= [ {_url} ]")
            if str(_url).startswith("/web/"):
                Log.i(f"Url is in way back machine. Fixing url.. [ {_url} ].")
                _url = way_back_machine_url + _url
            if self.stay_within != "" and self.stay_within in _url:
                if _url and str(_url).startswith("http"):
                    self.queue.add(_url)
                else:
                    Log.v(f"Not inside staywithin [ {_url} ]")

    def suicideCheck(self):
        if self.suicideSwitch and self.queue.isFull():
            Log.i("Queue is FULL! Changing MODE to SUICIDE.")
            self.change_mode(Modes.SUICIDE)

    def killThySelf(self):
        raise KillThySelf("Kill Order Initiated.")

    def print_status(self):
        print("\n")
        Log.i(f"---------------------------------------------")
        # Log.i(f"Time: {DATE.to_hours_minutes_seconds(self.timer.current_time())} Hours:Minutes:Seconds.")
        Log.i(f"Spider Queue: {self.queue.size()}")
        Log.i(f"Extraction Success: {len(self.extraction_success)}")
        Log.i(f"Extraction Failed: {len(self.extraction_failed)}")
        Log.i(f"---------------------------------------------")
        print("\n")


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
    # if guard in guardian:
    #     print(True)
    # c = ArchiveCrawler(engadget)
