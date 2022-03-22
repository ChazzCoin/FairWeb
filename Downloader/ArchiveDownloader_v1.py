from FWEB import DATE, LIST, HttpRequest, Soup, Tag, Log, URL, Regex, Language
import json
import sys

Log = Log("FWEB.Downloader.ArchiveDownloader_v1")

class Extract:
    response = None
    status = False
    soup = None
    # ->
    h_source = ""
    h_url = ""
    h_source_url = ""
    h_imgUrl = ""
    h_title = ""
    h_date = ""
    h_description = ""
    h_body = ""
    h_tags = []
    json = {}

    def __init__(self):
        sys.setrecursionlimit(5000)

    def start_url(self, url):
        self.h_url = url
        self.h_source = URL.get_site_name(url)
        self.h_source_url = f"www.{self.h_source}.com"
        self.request()
        if self.status:
            self.to_html()
            self.extract_data()
            self.to_json()
            print(json.dumps(self.json, indent=4, default=str))
        else:
            Log.i("Request was rejected by Server.")

    def start_soup(self, soup):
        if not soup:
            Log.e("Soup is Empty or None.")
        self.soup = soup
        self.extract_data()
        self.to_json()
        print(json.dumps(self.json, indent=4, default=str))

    # -> Step One -> Call URL and get Raw HTML back in Response Object.
    def request(self):
        Log.i(f"Making Request to URL = [ {self.h_url} ]")
        resp = HttpRequest.get_request(self.h_url)
        if resp:
            self.response = LIST.get(1, resp)

    # -> Step Two -> Convert Response Object to HTML Object
    def to_html(self):
        Log.i(f"Parsing Response Text to HTML Objects.")
        self.soup = Soup.Parse(self.response)

    # -> Step Four -> Extract Data from Elements/Tags
    def extract_data(self):
        Log.i(f"Attempting to Extract Data from HTML Elements.")
        self.get_date()
        self.get_title()
        self.get_img_url()
        self.get_body()

    """
        -> Get Attributes
    """
    def get_date(self):
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
                    self.h_date = date
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
        date = DATE.parse_date(potential_date)
        if date:
            self.h_date = date
            return True
        return False

    def get_title(self):
        try:
            text = self.soup.tag_h1.text
            self.h_title = text
        except Exception as e:
            Log.e(f"Unable to get Text from tag_h1.", error=e)
            self.h_title = "UNKNOWN"

    def get_body(self):
        if self.soup.element_p1:
            for p1_item in self.soup.element_p1:
                self.h_body = Language.combine_args_str(self.h_body, "\n", self.get_safe_text(p1_item))

    def get_safe_text(self, obj):
        try:
            return obj.text
        except Exception as e:
            Log.e("Failed to get Text", error=e)
            return "False"

    def get_img_url(self):
        if self.soup.element_img:
            attemptOne = self.get_img_url_one()
            if attemptOne:
                return True
            attemptTwo = self.get_img_url_two("data-src")
            if attemptTwo:
                return True
            attemptThree = self.get_img_url_two("src")
            if attemptThree:
                return True
            return False

    def get_img_url_one(self):
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
                    self.h_imgUrl = i_url
                    return True
            return False
        except Exception as e:
            Log.e("Failed to get img.", error=e)
            return False

    def get_img_url_two(self, key):
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
                    self.h_imgUrl = i_url
                    return True
            return False
        except Exception as e:
            Log.e("Failed to get img.", error=e)
            return False

    def to_json(self):
        self.json = {
            "title": self.h_title,
            "source": self.h_source,
            "url": self.h_url,
            "source_url": self.h_source_url,
            "imgUrl": self.h_imgUrl,
            "published_date": self.h_date,
            "body": self.h_body,
            "tags": self.h_tags
        }

# if __name__ == '__main__':
#     " 1 - 7, 9, 10, 15, 16 "
#     " denied by server = 8, 13 "
#     " Reddit = 11, 12, 14 "
#     newTest = "https://www.americanbanker.com/payments/news/inside-ripples-plans-for-mainstream-crypto-payments"  # denied
#     newTest1 = "https://blockworks.co/new-crypto-venture-capital-fund-investing-only-in-near-in-nod-to-specialization/"  # denied
#     newTest2 = "https://towardsdatascience.com/a-step-by-step-guide-to-scheduling-tasks-for-your-data-science-project-d7df4531fc41"
#     newTest3 = "https://www.americanbanker.com/payments/news/inside-ripples-plans-for-mainstream-crypto-payments"
#     d = Extract(newTest3)
#     temp = d.json
    # hookup = Parser.parse(temp)
    # print(validateAndSave(saveArchives=True, setDateToToday=False, hookup=hookup))
