from F import DICT

from FNLP import URL
from FNLP.Language import Utils
from FNLP.Regex import Re, ReDate
from F import LIST
from F import DATE
from FW.Core import HttpRequest, Tag, Soup
from F.LOG import Log
from dateutil import parser
import sys

Log = Log("Core.Extractor")

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
         "source_url", "img_url", "title",
         "date", "description", "body", "keywords"]

def ExtractDate(url):
    """ Convenience Method """
    return Extractor.Extract_PublishedDate(url)

def ExtractDateFromHTML(RawHTML):
    """ Convenience Method """
    try:
        return Extractor.Extract_PublishedDateFromRawHTML(RawHTML=RawHTML)
    except Exception as e:
        Log.e("Failed to extract publish date.", error=e)
        return False

class Extractor:
    base_url = ""
    isReddit = False
    subReddit = None
    soup = None
    data = {}

    @classmethod
    def Extract(cls, soup, url, client=False):
        sys.setrecursionlimit(10000)
        newCls = cls()
        newCls.base_url = URL.extract_base_url(url)
        newCls.set_data("client", client)
        if Re.contains("reddit", url):
            newCls.isReddit = True
            newCls.subReddit = URL.extract_sub_reddit(url)
            newCls.set_data("subreddit", newCls.subReddit)
        newCls.soup = soup
        newCls.build_json()
        return newCls

    @classmethod
    def Extract_PublishedDate(cls, url):
        sys.setrecursionlimit(10000)
        newCls = cls()
        # soup = HttpRequest.request_to_html(url)
        soup2 = HttpRequest.get_request_3k_to_html(url)
        newCls.soup = soup2
        newCls.base_url = URL.extract_base_url(url)
        if Re.contains("reddit", url):
            newCls.isReddit = True
            newCls.subReddit = URL.extract_sub_reddit(url)
            newCls.set_data("subreddit", newCls.subReddit)
        if newCls.date():
            return newCls.data["published_date"]
        return False

    @classmethod
    def Extract_PublishedDateFromRawHTML(cls, RawHTML):
        if not RawHTML:
            return False
        sys.setrecursionlimit(10000)
        newCls = cls()
        # soup = HttpRequest.request_to_html(url)
        newCls.soup = Soup.Parse(rawText=RawHTML)
        if newCls.date():
            date1 = DICT.get("published_date", newCls.data, False)
            if date1:
                return date1
            else:
                return DICT.get("date", newCls.data, False)
        return False

    def build_json(self):
        """  DYNAMIC {JSON/DICT} BUILDER  """
        self.data = {}
        for item in items:
            func = self.safe_get_att(item)
            if func:
                try:
                    func()
                except Exception as e:
                    Log.e(f"Failed to extract: {func}", error=e)

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
    def keywords(self):
        test_tag = self.soup.soup.findAll("meta")
        for item in test_tag:
            test = Tag.get_attribute(item, "name")
            if test and Re.contains_any(["keywords"], test):
                keywords = Tag.get_attribute(item, "content")
                self.set_data("keywords", keywords)
                return True
        return False

    # -> Date <- #
    def date(self):
        try:
            if self.isReddit:
                self.reddit_date()
                return True
            if self.master_date_extraction():
                return True
            if self.verify_date_found():
                return True
            return False
            # if self.soup.tag_body:
            #     if self.date_attempt_one():
            #         return True
            #     if self.date_attempt_two():
            #         return True
            #     if self.date_attempt_three():
            #         return True
            #     if self.date_attempt_four():
            #         return True
            #     if self.date_attempt_five():
            #         return True
            #     if self.date_attempt_six():
            #         return True
            #     return self.date_attempt_last()
        except Exception as e:
            Log.d(f"Date Extraction Failure. Error=[ {e} ]")
            return False

    def master_date_extraction(self):
        try:
            time_tag = self.soup.soup.find("time")
            if time_tag:
                time_attr = Tag.get_attribute(time_tag, "datetime")
                if time_attr and self.attempt_date_parse_set(time_attr):
                    return True
            return self.date_attempt_master_two()
        except Exception as e:
            Log.d(f"Failed to master extract date. Error=[ {e} ]")
            return False

    def verify_date_found(self):
        pdate = DICT.get("published_date", self.data, False)
        ndate = DICT.get("date", self.data, False)
        if pdate or ndate:
            return True
        return False

    def date_attempt_master_two(self):
        # temp_date = Tag.search(self.soup.element_meta, DATE_TAGS)
        # if temp_date:
        #     raw_date = self.get_content(temp_date)
        #     if self.attempt_date_parse_set(raw_date):
        #         return True
        return False

    def date_attempt_last(self):
        raw_str = str(self.soup.tag_time)
        extraction_attemt = ReDate.extract_date(raw_str)
        if extraction_attemt:
            if self.attempt_date_parse_set(extraction_attemt):
                return True
        raw_str = str(self.soup.tag_body)
        extraction_attemt = ReDate.extract_date(raw_str)
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
                date = ReDate.extract_date(text)
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

    def reddit_date(self):
        timestamp_tag = self.soup.soup.find("a", {"data-testid": "post_timestamp"})
        if timestamp_tag:
            date_ready = DATE.parse_reddit_timestamp_to_datetime(timestamp_tag.text)
            self.set_data("published_date", date_ready)

    def attempt_date_parse_set(self, potential_date):
        try:
            date = parse_date(potential_date)
            if date:
                self.set_data("published_date", date)
                return True
            return False
        except Exception as e:
            Log.e(f"Failed to parse date object. DateObj=[ {potential_date} ]", error=e)
            return False

    # -> Author <- #
    # @Ext.timelimit(3)
    def author(self):
        temp_author = Tag.search_element(self.soup.element_meta, ["og:author", "author"])
        if temp_author:
            author = self.get_content(temp_author)
            self.set_data("author", author)
        else:
            self.set_data("author", UNKNOWN)

    # -> Title <- #
    def title(self):
        try:
            title_tag = self.soup.soup.find('title')
            if title_tag:
                title_text = title_tag.string
                self.set_data("title", title_text)
                return
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
        if self.master_description():
            return True
        temp_description = Tag.search(self.soup.element_meta, ["og:description", "description"])
        if temp_description:
            descr = self.get_content(temp_description)
            self.set_data("description", descr)

    def master_description(self):
        description_tag = self.soup.soup.find("meta", {"name": "description"})
        if description_tag:
            desc_text = Tag.get_attribute(description_tag, "content")
            if desc_text:
                self.set_data("description", desc_text)
                return True
        return False

    # -> Body <- #
    def body(self):
        # -> If Reddit
        if self.isReddit:
            self.reddit_body()
        elif self.soup.element_p1:
            body = ""
            for p1_item in self.soup.element_p1:
                body = Utils.combine_args_str(body, "\n", self.get_safe_text(p1_item))
            self.set_data("body", body)

    def reddit_body(self):
        # -> Grab Main Post
        post_content = self.soup.soup.findAll("div", {"data-test-id": "post-content"})
        post = ""
        for item in post_content:
            innerTemp = Soup.safe_findAll(item, "p")
            if innerTemp:
                for innerItem in innerTemp:
                    post = Utils.combine_args_str(post, "\n", innerItem.text)
        # -> Grab Comments
        comment_content = self.soup.soup.findAll("div", {"data-testid": "comment"})
        comments = []
        for item in comment_content:
            innerTemp = Soup.safe_findAll(item, "p")
            comment = ""
            if innerTemp:
                for innerItem in innerTemp:
                    comment = Utils.combine_args_str(comment, "\n", innerItem.text)
                comments.append(comment)
        # -> Form Body
        body = post
        index = 1
        for com in comments:
            body = Utils.combine_args_str(body, f"\n\n -> COMMENT {index}: \n", com, "\n")
            index += 1
        self.set_data("body", body)

    def get_safe_text(self, obj):
        try:
            return obj.text
        except Exception as e:
            Log.e("Failed to get Text", error=e)
            return "False"

    # -> ImgUrl <- #

    def img_url(self):
        if self.isReddit and self.reddit_img_url():
            return True
        if self.master_img_url():
            return True
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

    def master_img_url(self):
        img_tags = self.soup.tag_body.findAll("img")
        if not img_tags:
            return False
        # -> Find Largest img Width in list of image tags.
        highest_width = 0
        highest_img = None
        for inner_img in img_tags:
            result = Tag.get_attribute(inner_img, "width")
            if result:
                result = str(result).replace("%", "")
                if int(result) > highest_width:
                    highest_width = int(result)
                    highest_img = inner_img
        # -> "src" as Key
        img_url_by_attribute = Tag.get_attribute(highest_img, "src")
        if img_url_by_attribute:
            self.set_data("imgUrl", img_url_by_attribute)
            return True
        # -> Convert to String, Regex for all URLS
        img_url_by_regex = URL.find_urls_in_str(highest_img)
        if img_url_by_regex:
            img_url = LIST.get(0, img_url_by_regex)
            self.set_data("imgUrl", img_url)
            return True
        return False

    def reddit_img_url(self):
        img_tags = self.soup.tag_body.findAll("img")
        if not img_tags:
            return False
        for inner_img in img_tags:
            result = Tag.get_attribute(inner_img, "alt")
            if result:
                if str(result).startswith(self.subReddit):
                    img_url = Tag.get_attribute(inner_img, "src")
                    self.set_data("imgUrl", img_url)
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
