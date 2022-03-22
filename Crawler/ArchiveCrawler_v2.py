import os
from bs4 import BeautifulSoup
from FWEB import FusedDownloader, HttpRequest, FQueue, DATE, DICT, URL, Log
Log = Log("FWEB.Crawler.ArchiveCrawler_v2")

way_back_machine_url = "https://web.archive.org"
avoid_list = ['youtube', 'twitter', 'facebook', 'instagram', 'advertising', 'apple', 'google',
              'spotify', 'tiktok', 'soundcloud', 'linkedin', 'flickr', 'oauth', 'terms-of-service',
              'privacy-policy', 'contact-us', 'fr', 'de']


class ArchiveCrawler:
    pid = None
    timer = None
    max = 100
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
        self.max = DICT.get("max", kwargs, default=100)
        self.pid = os.getpid()
        self.stay_within = URL.get_site_name(url)
        self.queue = FQueue(maxSize=self.max, avoidList=avoid_list)
        Log.i(f"Launching ArchiveCrawler with PID=[ {self.pid} ]")
        self.queue.add(url)
        Log.i(f"Ready to START: ArchiveCrawler PID=[ {self.pid} ]")

    def start(self):
        Log.i(f"STARTING: ArchiveCrawler PID=[ {self.pid} ]")
        self.run_spider_queue()

    def run_spider_queue(self):
        Log.i(f"Starting URL Queue with {self.queue.size()}.")
        # -> Clean Queue.
        if self.queue.size() > self.max / 2:
            Log.v("Cleaning Queue.")
            self.queue.clean()
        # -> Work Queue.
        while not self.queue.isEmpty():
            Log.v("Getting next item in Queue.")
            _url = self.queue.get()
            # -> Attempt Download
            self.attempt_download(_url)
            # -> Request
            self.request(_url)
            # -> Parse out URLs
            extracted_urls = self.extract_urls()
            # -> Add all URLs to Queue
            self.handle_extracted_urls(extracted_urls)
            # -> Run Extraction
            self.print_status()

    def attempt_download(self, url):
        Log.i("Starting Extraction Queue")
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
            response = HttpRequest.get_request(_url)
            self.soup = BeautifulSoup(response.text, 'html.parser')
            Log.v("Request Made")
        except Exception as e:
            Log.e("Failed to make request.", error=e)

    def extract_urls(self):
        Log.v("Extracting URLs via Soup.")
        return self.soup.findAll('a', href=True)

    def handle_extracted_urls(self, extracted_urls):
        Log.v("Looping extracted urls.")
        for item in extracted_urls:
            _url = item['href']
            if str(_url).startswith("/web/"):
                Log.v(f"Url is in way back machine. Fixing url.. [ {_url} ].")
                _url = way_back_machine_url + _url
            if self.stay_within != "" and self.stay_within in _url:
                if _url and str(_url).startswith("http"):
                    self.queue.add(_url)
                else:
                    Log.v(f"Not inside staywithin [ {_url} ]")

    def print_status(self):
        print("\n")
        Log.i(f"---------------------------------------------")
        Log.i(f"Time: {DATE.to_hours_minutes_seconds(self.timer.current_time())} Hours:Minutes:Seconds.")
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
    guard = "theguardian"
    marketwatch = "https://www.marketwatch.com/"
    imdb = "https://www.imdb.com/title/tt0110357/news?ref_=tt_ql_sm"
    cnet = "https://www.cnet.com/news/"
    verge = "https://www.theverge.com/tech"
    yahoo = "https://finance.yahoo.com/"
    engadget = "https://www.engadget.com/"
    # if guard in guardian:
    #     print(True)
    c = ArchiveCrawler(engadget).start()
