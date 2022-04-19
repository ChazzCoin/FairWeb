import gc
import os
from bs4 import BeautifulSoup

from Jarticle.jURL import jURL
from fwebUtils import DICT, URL, LIST
from Downloader import FusedDownloader
from fwebCore import HttpRequest
from FQueue.UrlQueue import FQueue
from fwebUtils.LOGGER import Log
Log = Log("FWEB.Crawler.ArchiveCrawler_v2")

way_back_machine_url = "https://web.archive.org"
avoid_list = ['youtube', 'twitter', 'facebook', 'instagram', 'advertising', 'apple', 'google',
              'spotify', 'tiktok', 'soundcloud', 'linkedin', 'flickr', 'oauth', 'terms-of-service',
              'privacy-policy', 'contact-us', 'fr', 'de', "coupon", "coupons", "search", "help",
              "login", "logout", "amazon", "policy", "policies", "mobile", "yimg", "mail", "oath"]


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
    QUEUED = "QUEUED"
    SUICIDE = "SUICIDE"
    KILL = "KILL"

class ArchiveCrawler:
    pid = None
    timer = None
    # -> kwargs
    max = 100
    suicideSwitch = False
    stayWithin = True
    # -> Global
    MODE = Modes.NORMAL
    queue: FQueue = None
    extraction_success = []
    extraction_failed = []
    base_url = ""
    stay_within = ""
    response = None
    soup = None
    total_count = 0

    def __init__(self, **kwargs):
        """
        -> Takes single URL, grabs every URL, then tries to download them all.
        -> Takes next URL, grabs every URL, tries to download them all.
        -> !Potential for Forever-Loop!
        """
        self.pid = os.getpid()
        Log.i(f"Launching ArchiveCrawler with PID=[ {self.pid} ]")
        self.handle_kwargs(**kwargs)
        self.queue = FQueue(maxSize=self.max, avoidList=avoid_list)
        Log.i(f"Ready to START: ArchiveCrawler PID=[ {self.pid} ]")

    def __del__(self):
        self.clean_mongo()
        gc.collect()

    def init_WithUrl(self, url):
        """
            -> Takes single URL, grabs every URL, then tries to download them all.
            -> Takes next URL, grabs every URL, tries to download them all.
            -> !Potential for Forever-Loop!
        """
        self.process_url(url)
        self.queue.add(url)
        return self

    def process_url(self, url):
        self.stay_within = URL.get_site_name(url)
        self.base_url = URL.extract_base_url(url)

    @classmethod
    def Start_WithUrl(cls, _url, **kwargs):
        cls(**kwargs).init_WithUrl(_url).run()

    @classmethod
    def start_NormalMode(cls, _url, **kwargs):
        kwargs["suicideMode"] = False
        cls(**kwargs).init_WithUrl(_url).run()

    @classmethod
    def start_SuicideMode(cls, _url, **kwargs):
        kwargs["suicideMode"] = True
        cls(**kwargs).init_WithUrl(_url).run()

    @classmethod
    def start_QUEUED(cls, **kwargs):
        kwargs["suicideMode"] = True
        kwargs["stayWithin"] = DICT.get("stayWithin", kwargs, default=False)
        kwargs["MODE"] = DICT.get("MODE", kwargs, default=Modes.SUICIDE)
        kwargs["max"] = DICT.get("max", kwargs, default=0)
        nc = cls(**kwargs)
        processing_queue = jURL.GET_FROM_QUEUED()
        if processing_queue:
            nc.add_all(processing_queue)
            nc.run()
            return True
        Log.e("No URLs from DB!")
        return False

    @classmethod
    def start_DEEP_MODE(cls, _url, **kwargs):
        kwargs["suicideMode"] = False
        kwargs["max"] = 0
        kwargs["stayWithin"] = False
        cls(**kwargs).init_WithUrl(_url).run()

    def handle_kwargs(self, **kwargs):
        self.max = DICT.get("max", kwargs, default=100)
        self.suicideSwitch = DICT.get("suicideMode", kwargs, default=False)
        self.MODE = DICT.get("MODE", kwargs, default=Modes.SUICIDE)
        self.stayWithin = DICT.get("stayWithin", kwargs, default=True)

    def run(self):
        Log.i(f"STARTING: ArchiveCrawler PID=[ {self.pid} ]")
        self.clean_mongo()
        self.run_spider_queue()
        self.clean_mongo()
        gc.collect()

    @staticmethod
    def clean_mongo():
        return jURL()

    def add_all(self, *urls):
        urls = LIST.flatten(urls)
        for url in urls:
            self.queue.add(url)

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
            current_url = self.queue.get()
            # -> Get/Set Request Response
            self.set_response(current_url)
            # -> Attempt Download
            self.attempt_download(current_url)
            # -> Begin to die? or Continue as Normal?
            if self.verify_mode():
                # -> Run URL Extraction
                self.extract_urls(current_url)
            self.print_status()

    def attempt_download(self, url):
        Log.i("Attempting Archive Download.")
        result = FusedDownloader.crawler_downloader(url, self.response)
        if result:
            Log.v("Extraction Success")
            self.extraction_success.append(url)
        else:
            Log.v("Extraction Failed")
            self.extraction_failed.append(url)

    def set_response(self, _url):
        try:
            Log.v("Making Request via requests and parsing html via bs4.")
            request_response = HttpRequest.get_request(_url)
            self.response = LIST.get(1, request_response)
            self.soup = BeautifulSoup(self.response.text, 'html.parser')
            Log.v("Request Made")
        except Exception as e:
            Log.e("Failed to make request.", error=e)

    def extract_urls(self, _url):
        # -> Parse out URLs
        if self.soup is None:
            return
        Log.v("Extracting URLs via Soup.")
        # 1. Soup Based URLs
        soup_urls = self.find_urls_in_soup()
        # 2. Regex Based URLs
        regex_urls = URL.find_urls_in_str(str(self.soup))
        # 3. Combined All URLs
        urls = soup_urls + regex_urls
        # -> Add all URLs to Queue
        filtered_urls = self.handle_extracted_urls(urls)
        self.add_urls_to_queue(filtered_urls)

    def find_urls_in_soup(self):
        soup_refs = self.soup.findAll('a', href=True)  # 1. Soup->Tag
        soup_urls = []
        for item in soup_refs:
            href_url = DICT.get("href", item)
            if str(href_url).startswith("/"):
                href_url = "https://" + self.base_url + href_url
            soup_urls.append(href_url)
        return soup_urls

    @staticmethod
    def filter_extracted_urls(extracted_urls):
        extracted_urls = list(set(extracted_urls))
        extracted_urls = URL.filter_out_bad_exts(extracted_urls)
        extracted_urls = URL.filter_out_avoid_list(extracted_urls, avoid_list)
        return extracted_urls

    def handle_extracted_urls(self, extracted_urls):
        if not extracted_urls:
            Log.i("No Extracted URLS")
            return
        Log.i("Looping extracted urls.")
        extracted_urls = self.filter_extracted_urls(extracted_urls)
        jURL.ADD_TO_QUEUED(extracted_urls)
        return extracted_urls

    def add_urls_to_queue(self, extracted_urls):
        if not extracted_urls:
            Log.i("No Extracted URLS")
            return
        for ex_url in extracted_urls:
            if self.queue.isFull():
                Log.i("Queue is FULL!")
                return
            Log.d(f"Looking at URL= [ {ex_url} ]")
            # -> TODO: Check WayBackMachine ...
            if str(ex_url).startswith("/web/"):
                Log.i(f"Url is in way back machine. Fixing url.. [ {ex_url} ].")
                ex_url = way_back_machine_url + ex_url
            if self.check_stay_within():
                if self.stay_within != "" and self.stay_within in ex_url:
                    if ex_url and URL.is_url(ex_url):
                        self.queue.add(ex_url)
                        continue
                    else:
                        Log.v(f"Not inside staywithin [ {ex_url} ]")
                        continue
                else:
                    continue
            # If all else fails, add it.
            if ex_url and URL.is_url(ex_url):
                self.queue.add(ex_url)

    def mode_add(self, url):
        if self.MODE == Modes.QUEUED:
            jURL.ADD_TO_QUEUED(url)
            return
        self.queue.add(url)

    def mode_pop(self):
        if self.MODE == Modes.QUEUED:
            return jURL.GET_FROM_QUEUED()
        return self.queue.get()

    def check_stay_within(self):
        return self.stayWithin

    def suicideCheck(self):
        if self.suicideSwitch and self.queue.isFull():
            Log.i("Queue is FULL! Changing MODE to SUICIDE.")
            self.change_mode(Modes.SUICIDE)

    def killThySelf(self):
        self.clean_mongo()
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
    download = "https://www.medium.com"
    ArchiveCrawler.start_QUEUED(stayWithin=False)
    # if guard in guardian:
    #     print(True)
    # c = ArchiveCrawler(engadget)
