from bs4 import BeautifulSoup
from bs4.element import Tag as bsTag
from FWEB import Tag, Log
Log = Log("Clients.Archive.ArchiveDownloader_v2")


# -> Step Two -> Convert Response Object to HTML Object
def to_html(response):
    return BeautifulSoup(response.text, 'html.parser')

def safe_find(tag, term):
    try:
        return tag.find(term)
    except Exception as e:
        Log.e("Failed to find term.", error=e)


def safe_findAll(tag, term):
    try:
        return tag.find(term)
    except Exception as e:
        Log.e("Failed to find term.", error=e)

class Parse:
    response = None
    status = False
    soup = None
    tag_body: bsTag = None
    tag_time: bsTag = None
    element_img = None
    element_p1 = None
    tag_h1: bsTag = None
    element_meta = None
    element_span = None

    def __init__(self, response):
        self.response = response
        self.to_html()
        self.extract_elements_and_tags()

    # -> Step Two -> Convert Response Object to HTML Object
    def to_html(self):
        self.soup = BeautifulSoup(self.response.text, 'html.parser')

    # -> Step Three -> Convert HTML into Element/Tag Objects
    def extract_elements_and_tags(self):
        Log.i(f"Extracting HTML Elements.")
        self.tag_body = safe_find(self.soup, "body")  # -> 99%
        self.tag_time = safe_find(self.tag_body, "time")  # ->
        self.element_img = safe_findAll(self.tag_body, "img")
        self.element_p1 = safe_findAll(self.tag_body, "p")  # ->
        self.tag_h1 = safe_find(self.tag_body, "h1")  # ->
        self.element_meta = safe_findAll(self.soup, "meta")
        self.element_span = safe_findAll(self.tag_body, "span")
        Log.i("Parsing Finished")

if __name__ == '__main__':
    test1 = "https://public.totalglobalsports.com/public/event/2038/game-complex/466/1653/35242"
    test = "https://public.totalglobalsports.com/public/event/2038/individual-team/18/35266/9"
    s = Parse(test1)
    result = Tag.search_tag_deep(s.tag_body, "tbody", enableName=True)
    print(result)