from bs4 import BeautifulSoup
from bs4.element import Tag as bsTag
from F.LOG import Log
Log = Log("FairWeb.Core.Soup.Parse()")

# -> Step Two -> Convert Response Object to HTML Object
def to_html_from_response(response):
    return BeautifulSoup(response.text, 'html.parser')

def to_html_from_text(text):
    return BeautifulSoup(text, 'html.parser')

def safe_find(tag, term):
    try:
        return tag.find(term)
    except Exception as e:
        Log.e("Failed to find term.", error=e)

def safe_findAll(tag, term):
    try:
        return tag.findAll(term)
    except Exception as e:
        Log.e("Failed to find term.", error=e)

class Parse:
    response = None
    status = False
    soup = None
    raw_text = None
    tag_body: bsTag = None
    tag_head: bsTag = None
    tag_time: bsTag = None
    element_img = None
    element_p1 = None
    tag_h1: bsTag = None
    element_meta = None
    element_span = None

    def __init__(self, response=None, rawText=None):
        self.response = response
        self.raw_text = rawText
        if rawText:
            if self.to_html_from_raw_text():
                self.extract_elements_and_tags()
        elif self.to_html():
            self.extract_elements_and_tags()

    # -> Step Two -> Convert Response Object to HTML Object
    def to_html(self):
        if self.response:
            self.soup = BeautifulSoup(self.response.text, 'html.parser')
            return True
        else:
            return False

    def to_html_from_raw_text(self):
        if self.raw_text:
            self.soup = BeautifulSoup(self.raw_text, 'html.parser')
            return True
        else:
            return False

    # -> Step Three -> Convert HTML into Element/Tag Objects
    def extract_elements_and_tags(self):
        Log.i(f"Extracting HTML Elements.")
        self.tag_body = safe_find(self.soup, "body")  # -> 99%
        self.tag_head = safe_find(self.soup, "head")  # -> 99%
        self.tag_time = safe_find(self.tag_body, "time")  # ->
        self.element_img = safe_findAll(self.tag_body, "img")
        self.element_p1 = safe_findAll(self.soup, "p")  # ->
        self.tag_h1 = safe_find(self.tag_body, "h1")  # ->
        self.element_meta = safe_findAll(self.tag_head, "meta")
        self.element_span = safe_findAll(self.tag_body, "span")
        self.doTest()
        Log.i("Parsing Finished")

    def doTest(self):
        pass
        # for tr in self.soup.find_all('tr')[2:]:
        #     tds = tr.find_all('td')
        #     print("Nome: %s, Cognome: %s, Email: %s" + "% tds[0].text, tds[1].text, tds[2].text")
        # pass
