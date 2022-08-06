import os

from FW.Crawler import UrlProcess
from FW.Crawler import UrlExtractor
from F import DICT
from FNLP import URL
from FW.Core import HttpRequest
from FW.Crawler.UrlQueue import FQueue
from F.LOG import Log
Log = Log("FWEB.Crawler.ArchiveCrawler_v2")

way_back_machine_url = "https://web.archive.org"
avoid_list = ['youtube', 'twitter', 'facebook', 'instagram', 'advertising', 'apple', 'google',
              'spotify', 'tiktok', 'soundcloud', 'linkedin', 'flickr', 'oauth', 'terms-of-service',
              'privacy-policy', 'contact-us', '.fr', '.de', "coupon.", "coupons.", ".coupon", ".coupons",
              ".chinese", "chinese.", ".japan", "japan.", ".kr", ".fr", ".getinvisiblehand"]

MAX_QUEUE = 100

CRAWLER_VERSION = "3.0.0"

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
    original_url = None
    current_base_url = None
    # -> kwargs
    max = MAX_QUEUE
    suicideSwitch = False
    saveToDB = True
    # -> Global
    MODE = Modes.NORMAL
    queue: FQueue = None
    extraction_success = []
    extraction_failed = []
    stay_within = ""
    soup = None
    total_count = 0
    base_site = ""
    # -> Alternative Output
    articles = []

    def __init__(self, url, **kwargs):
        """
        -> Takes single URL, grabs every URL, then tries to download them all.
        -> Takes next URL, grabs every URL, tries to download them all.
        -> !Potential for Forever-Loop!
        """
        self.handle_kwargs(**kwargs)
        self.pid = os.getpid()
        self.original_url = url
        self.stay_within = URL.get_site_name(url)
        self.base_site = URL.get_base_url(url)
        self.current_base_url = self.base_site
        self.queue = FQueue(maxSize=self.max, avoidList=avoid_list)
        Log.i(f"Launching ArchiveCrawler. URL=[ {url} ] PID=[ {self.pid} ]")
        self.queue.add(url)
        Log.i(f"Ready to START: ArchiveCrawler PID=[ {self.pid} ]")

    """
            -> GLOBAL CRAWLER INIT & RUN HELPERS
        1. Input URL and everything else is pre-setup.
    """

    @classmethod
    def start_UnlimitedMode(cls, _url, **kwargs):
        kwargs["suicideMode"] = False
        newClass = cls(_url, **kwargs)
        newClass.run()
        return newClass

    @classmethod
    def start_SuicideMode(cls, _url, **kwargs):
        kwargs["suicideMode"] = True
        newClass = cls(_url, **kwargs)
        newClass.run()
        return newClass

    """
        -> INIT HELPERS
    1. Set Global Configurations.
        - 'max' = Max number of URL's allowed into queue.
        - 'suicideMode' = Once 'max' is reached, crawler will empty queue and end/die.
    2. Run Main Queue Loop Process.
    """

    def handle_kwargs(self, **kwargs):
        self.max = DICT.get("max", kwargs, default=MAX_QUEUE)
        self.suicideSwitch = DICT.get("suicideMode", kwargs, default=False)
        self.saveToDB = DICT.get("saveToDB", kwargs, default=True)

    def run(self):
        Log.i(f"STARTING: ArchiveCrawler PID=[ {self.pid} ]")
        self.run_spider_queue()

    """
        -> MAIN CRAWLER PROCESS/LOOP
    1. Loop Main Queue until Empty.
    2. Process/Download URL into Article.
    3. Extract all further URL's from current URL's HTML.
    """

    """ (Crawler.UrlQueue.py) -> 1. Start: Run Queue until Empty """
    def run_spider_queue(self):
        Log.i(f"Starting URL Queue with {self.queue.size()}.")
        while not self.queue.isEmpty():
            self.total_count += 1
            # -> Clean Queue Check.
            if self.queue.size() > self.max / 2:
                Log.v("Cleaning Queue.")
                self.queue.clean()
            Log.v("Popping URL from Main Queue.")
            _url = self.queue.get()
            Log.i(f"Current URL = [ {_url} ]")
            if not self.stay_within:
                self.current_base_url = URL.get_base_url(_url)
            self.url_process(_url)
            # -> Begin to die? or Continue as Normal?
            if self.verify_mode():
                # -> Run URL Extraction
                self.url_extractor(_url)
            # -> Print Current Status for Developer
            self.print_status()
        # -> The End.
        return self

    """ (Crawler.UrlProcess.py) -> 2. Process URL """
    def url_process(self, _url):
        # -> Attempt Download
        result = UrlProcess.attempt_download(_url, self.saveToDB)
        if result:
            if not self.saveToDB:
                self.articles.append(result)
            self.extraction_success.append(_url)
        else:
            self.extraction_failed.append(_url)

    """ (Crawler.UrlExtractor.py) -> 3. Extract all URLs from current URLs WebPage. """
    def url_extractor(self, _url):
        # -> Request HTML and Parse into Soup Object.
        self.soup = HttpRequest.get_request_3k_to_html(_url, parseToSoup=True)
        if self.soup is None:
            return False
        Log.v("Extracting URLs via Url Extractor.")
        if self.soup.soup:
            extracted_urls = UrlExtractor.extract_urls_from_soup(self.soup.soup, self.current_base_url, stayWithin=self.stay_within)
        else:
            extracted_urls = UrlExtractor.extract_urls_from_soup(self.soup, self.current_base_url, stayWithin=self.stay_within)
        # -> Add all URLs to Queue
        if extracted_urls:
            self.queue.add_list(extracted_urls)
        return True

    """
    -> HELPERS
    """

    def verify_mode(self):
        """ Check Mode. """
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

    def suicideCheck(self):
        """
        If suicideMode,
        check if crawler needs to switch
        to turning off the queue and emptying queue
        or not.
        """
        if self.suicideSwitch:
            queue_count = self.queue.size()
            if self.queue.isFull() \
                    or queue_count >= self.max - 1\
                    or self.total_count >= self.max:
                Log.i("Queue is FULL! Changing MODE to SUICIDE.")
                self.change_mode(Modes.SUICIDE)

    def killThySelf(self):
        """ Immediately cause a fetal error and end system process. """
        raise KillThySelf("Kill Order Initiated.")

    """
    -> Print/Log Status for Developer
    """
    def print_status(self):
        Log.i(f"---------------------------------------------")
        # Log.i(f"Time: {DATE.to_hours_minutes_seconds(self.timer.current_time())} Hours:Minutes:Seconds.")
        Log.i(f"Crawler Mode: {self.MODE}")
        Log.i(f"Spider Queue Size: {self.queue.size()}")
        Log.i(f"Total URLs Crawled: {self.total_count}")
        Log.i(f"Article Success: {len(self.extraction_success)}")
        Log.i(f"Article Failed: {len(self.extraction_failed)}")
        Log.i(f"---------------------------------------------")



