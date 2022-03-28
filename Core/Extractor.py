from FWEB.Futils import URL, Regex, Language, LIST, Ext
from FWEB.Core import Tag
from FWEB.rsLogger import Log
from dateutil import parser

Log = Log("FWEB.Core.Extractor")

DATE_TAGS = ['rnews:datePublished', 'article:published_time', 'OriginalPublicationDate',
             'datePublished', 'og:published_time', 'article_date_original',
             'publication_date', 'sailthru.date', 'PublishDate', 'pubdate',
             'og:published_time', 'og:pubdate', 'published_time', 'date']

DESCRIPTION_TAGS = ["og:description", "description"]

NO_STRINGS = set()
A_REL_TAG_SELECTOR = "a[rel=tag]"
A_HREF_TAG_SELECTOR = ("a[href*='/tag/'], a[href*='/tags/'], "
                       "a[href*='/topic/'], a[href*='?keyword=']")
RE_LANG = r'^[A-Za-z]{2}$'

good_paths = ['story', 'article', 'feature', 'featured', 'slides',
              'slideshow', 'gallery', 'news', 'video', 'media',
              'v', 'radio', 'press']
bad_chunks = ['careers', 'contact', 'about', 'faq', 'terms', 'privacy',
              'advert', 'preferences', 'feedback', 'info', 'browse', 'howto',
              'account', 'subscribe', 'donate', 'shop', 'admin']
bad_domains = ['amazon', 'doubleclick', 'twitter']

s = " "
UNKNOWN = "UNKNOWN"
# -> Master Parser
def parse_str(obj: str):
    return parser.parse(obj)

def parse_date(obj=None):
    try:
        if type(obj) is str:
            obj = parse_str(obj)
        elif type(obj) is list:
            return None
        p_date = str(obj.strftime("%B")) + s + str(obj.strftime("%d")) + s + str(obj.strftime("%Y"))
        return p_date
    except Exception as e:
        print(e)
        return False

items = ["author", "source", "url",
         "source_url", "imgUrl", "title",
         "date", "description", "body", "tags"]

class Extractor:
    soup = None
    data = {}

    @classmethod
    def Extract(cls, soup):
        newCls = cls()
        newCls.soup = soup
        newCls.build_json()
        return newCls

    def build_json(self):
        """  DYNAMIC {JSON/DICT} BUILDER  """
        self.extract_tags(self.soup.tag_body)
        for item in items:
            func = self.safe_get_att(item)
            if func:
                func()

    def set_data(self, key, value):
        self.data[key] = value

    def safe_get_att(self, attr):
        try:
            item = getattr(self, attr)
            return item
        except Exception as e:
            Log.e("Failed to get attribute/function.", error=e)
            return False

    @staticmethod
    def get_content(search_results):
        temp_tag = LIST.get(2, search_results)
        temp_value = Tag.get_value_for_key(temp_tag, "content")
        return temp_value

    """
        -> Get Attributes
    """

    # -> Date <- #

    def date(self):
        if self.master_date_extraction():
            return True
        if self.soup.tag_body:
            attemptOne = self.date_attempt_one()
            if attemptOne:
                return True
            attemptTwo = self.date_attempt_two()
            if attemptTwo:
                return True
            attemptThree = self.date_attempt_three()
            if attemptThree:
                return True
            attemptFour = self.date_attempt_four()
            if attemptFour:
                return True
            attemptFive = self.date_attempt_five()
            if attemptFive:
                return True
            attemptSix = self.date_attempt_six()
            if attemptSix:
                return True
            attemptLast = self.date_attempt_last()
            if attemptLast:
                return True
            return False

    def master_date_extraction(self):
        temp_date = Tag.search(self.soup.element_meta, DATE_TAGS)
        if temp_date:
            raw_date = self.get_content(temp_date)
            if self.attempt_date_parse_set(raw_date):
                return True
        return False

    def date_attempt_last(self):
        raw_str = str(self.soup.tag_time)
        extraction_attemt = Regex.extract_date(raw_str)
        if extraction_attemt:
            if self.attempt_date_parse_set(extraction_attemt):
                return True
        raw_str = str(self.soup.tag_body)
        extraction_attemt = Regex.extract_date(raw_str)
        if extraction_attemt:
            if self.attempt_date_parse_set(extraction_attemt):
                return True
        return False

    def date_attempt_one(self):
        temp_date = Tag.search(self.soup.tag_body, ["datetime", "dateCreated"], enableAttributes=True)
        if temp_date:
            if self.attempt_date_parse_set(LIST.get(1, temp_date)):
                return True
        return False

    def date_attempt_two(self):
        temp_date = Tag.search(self.soup.tag_body, ["update-time"], enableAttributes=True)
        temp_text = Tag.get_text(LIST.get(2, temp_date))
        if temp_text:
            if self.attempt_date_parse_set(temp_date):
                return True
        return False

    def date_attempt_three(self):
        temp_date = Tag.search(self.soup.tag_body, ["datetime", "dateCreated"], enableAttributes=True)
        content = Tag.get_attribute(LIST.get(2, temp_date), "content")
        if content:
            if self.attempt_date_parse_set(content):
                return True
        return False

    def date_attempt_four(self):
        temp_date = Tag.search(self.soup.tag_body, ["published-date"], enableAttributes=True)
        content = Tag.get_text(LIST.get(2, temp_date))
        if content:
            if self.attempt_date_parse_set(content):
                return True
        return False

    def date_attempt_five(self):
        """ Loops through ALL Span Elements Tags -> Text """
        for tag in self.soup.element_span:
            text = Tag.get_text(tag)
            if text:
                date = Regex.extract_date(text)
                if date:
                    self.set_data("date", date)
                    return True
        return False

    def date_attempt_six(self):
        temp_date = Tag.search_tag_deep(self.soup.tag_body, ["datePublished"], enableAttributes=True)
        temp_text = Tag.get_text(LIST.get(2, temp_date))
        if temp_text:
            if self.attempt_date_parse_set(temp_text):
                return True
        return False

    def attempt_date_parse_set(self, potential_date):
        date = parse_date(potential_date)
        if date:
            self.set_data("date", date)
            return True
        return False

    # -> Author <- #

    def author(self):
        temp_author = Tag.search(self.soup.element_meta, ["og:author", "author"])
        if temp_author:
            author = self.get_content(temp_author)
            self.set_data("author", author)
        else:
            self.set_data("author", UNKNOWN)

    # -> Title <- #

    def title(self):
        try:
            text = self.soup.tag_h1.text
            self.set_data("title", text)
            if not text or text == "":
                if not self.get_meta_title():
                    self.set_data("title", UNKNOWN)
        except Exception as e:
            Log.e(f"Unable to get Text from tag_h1. Attempting META Extraction.", error=e)
            if not self.get_meta_title():
                self.set_data("title", UNKNOWN)

    def get_meta_title(self):
        temp_title = Tag.search(self.soup.element_meta, ["og:title", "title"])
        if temp_title:
            self.set_data("title", self.get_content(temp_title))
            return True
        return False

    # -> Description <- #

    def description(self):
        temp_description = Tag.search(self.soup.element_meta, ["og:description", "description"])
        if temp_description:
            descr = self.get_content(temp_description)
            self.set_data("description", descr)

    # -> Body <- #

    def body(self):
        if self.soup.element_p1:
            body = ""
            for p1_item in self.soup.element_p1:
                body = Language.combine_args_str(body, "\n", self.get_safe_text(p1_item))
            self.set_data("body", body)

    def get_safe_text(self, obj):
        try:
            return obj.text
        except Exception as e:
            Log.e("Failed to get Text", error=e)
            return "False"

    # -> ImgUrl <- #

    def imgUrl(self):
        if self.soup.element_img:
            attemptOne = self.attempt_img_url_one()
            if attemptOne:
                return True
            attemptTwo = self.attempt_img_url_two("data-src")
            if attemptTwo:
                return True
            attemptThree = self.attempt_img_url_two("src")
            if attemptThree:
                return True
            return False

    def attempt_img_url_one(self):
        try:
            img_results = Tag.search(self.soup.element_img, "img", enableName=True)
            src_results = Tag.search_attributes(LIST.get(2, img_results), "src")
            potential_url = LIST.get(1, src_results)
            split_url = potential_url.split(" ")
            is_url = URL.is_url(split_url)
            if LIST.get(0, is_url):
                i_url = LIST.get(1, is_url)
                test = URL.is_valid_url(i_url)
                if test:
                    self.set_data("imgUrl", i_url)
                    return True
            return False
        except Exception as e:
            Log.e("Failed to get img.", error=e)
            return False

    def attempt_img_url_two(self, key):
        try:
            img_results = Tag.search(self.soup.element_img, "img", enableName=True)
            if not img_results:
                return False
            src_results = Tag.get_attribute(LIST.get(2, img_results), key)
            if not src_results:
                return False
            potential_url = URL.extract_data_src_url(str(src_results))
            is_url = URL.is_url(potential_url)
            if LIST.get(0, is_url):
                i_url = LIST.get(1, is_url)
                test = URL.is_valid_url(i_url)
                if test:
                    self.set_data("imgUrl", i_url)
                    return True
            return False
        except Exception as e:
            Log.e("Failed to get img.", error=e)
            return False

    def extract_tags(self, tag):
        if len(list(tag)) == 0:
            return NO_STRINGS
        elements = tag.cssselect(
            tag, A_REL_TAG_SELECTOR)
        if not elements:
            elements = tag.cssselect(
                tag, A_HREF_TAG_SELECTOR)
            if not elements:
                return NO_STRINGS

        tags = []
        for el in elements:
            tag = [i for i in el.itertext()]
            if tag:
                tags.append(tag)
        return set(tags)