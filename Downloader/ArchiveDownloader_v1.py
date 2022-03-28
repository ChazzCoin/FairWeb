from FWEB.Futils import URL, LIST
from FWEB.Core import HttpRequest, Soup, Extractor
from FWEB.Core.Extractor import Extractor
from FWEB.rsLogger import Log
import json
import sys

Log = Log("FWEB.Downloader.ArchiveDownloader_v1")

class DownloadWebPage:
    response = None
    status = False
    soup = None
    # ->
    url = ""
    json = {}

    def __init__(self):
        sys.setrecursionlimit(5000)

    @classmethod
    def start_url(cls, url):
        newExtractor = cls()
        newExtractor.url = url
        newExtractor.request()
        if newExtractor.response:
            newExtractor.to_html()
            newExtractor.extract_data()
            print(json.dumps(newExtractor.json, indent=4, default=str))
            return newExtractor
        else:
            Log.i("Request was rejected by Server.")
            return False

    def start_soup(self, soup):
        if not soup:
            Log.e("Soup is Empty or None.")
        self.soup = soup
        self.extract_data()
        # self.to_json()
        print(json.dumps(self.json, indent=4, default=str))

    # -> Step One -> Call URL and get Raw HTML back in Response Object.
    def request(self):
        Log.i(f"Making Request to URL = [ {self.url} ]")
        resp = HttpRequest.get_request(self.url)
        if resp:
            self.response = LIST.get(1, resp)

    # -> Step Two -> Convert Response Object to HTML Object
    def to_html(self):
        Log.i(f"Parsing Response Text to HTML Objects.")
        self.soup = Soup.Parse(self.response)

    # -> Step Four -> Extract Data from Elements/Tags
    def extract_data(self):
        Log.i(f"Attempting to Extract Data from HTML Elements.")
        temp = Extractor.Extract(self.soup)
        self.json = temp.data
        self.set_json("url", self.url)
        source = URL.get_site_name(self.url)
        self.set_json("source", source)
        self.set_json("source_url", f"www.{source}.com")

    def set_json(self, key, value):
        self.json[key] = value

if __name__ == '__main__':
    newTest = "https://towardsdatascience.com/how-to-use-qgis-spatial-algorithms-with-python-scripts-4bf980e39898"  # denied
    newTest1 = "https://www.cnn.com/2022/03/27/politics/joe-biden-vladimir-putin-ukraine-war/index.html"  # denied
    newTest2 = "https://towardsdatascience.com/a-step-by-step-guide-to-scheduling-tasks-for-your-data-science-project-d7df4531fc41"
#     newTest3 = "https://www.americanbanker.com/payments/news/inside-ripples-plans-for-mainstream-crypto-payments"
    d = DownloadWebPage.start_url(url=newTest2)

