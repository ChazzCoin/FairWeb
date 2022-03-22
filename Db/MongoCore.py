from pymongo import MongoClient
from pymongo.database import Database
from FWEB.Db import fig
from dateutil import parser
from FWEB import DATE, DICT, Log
import datetime
Log = Log("FWEB.Db.MongoCore")

s = " "

# if MongoConfig.db_environment == MongoConfig.LOCAL:
#     MONGO_URI = MongoConfig.local_mongo_db_uri
# elif MongoConfig.db_environment == MongoConfig.SOZIN:
#     MONGO_URI = MongoConfig.sozin_mongo_db_uri
# else:
#     MONGO_URI = MongoConfig.prod_mongo_db_uri


class MongoCore:
    client: MongoClient
    master: Database
    c_news: Database
    c_archive: Database
    c_hookups: Database
    c_words: Database
    c_urls: Database

    def __init__(self, url=fig.local_mongo_db_uri):
        Log.i(f"Initiating MongoDB at url={url}")
        try:
            self.client = MongoClient(url)
        except Exception as e:
            Log.e("Unable to initiate MongoDB.", error=e)
            return
        self.master = self.client.get_database("research")
        self.c_news = self.master.get_collection("news")
        self.c_archive = self.master.get_collection("archive")
        self.c_hookups = self.master.get_collection("hookups")
        self.c_words = self.master.get_collection("words")
        self.c_urls = self.master.get_collection("urls")

    def get_var(self, var_name):
        """  GETTER HELPER  """
        return self.__getattribute__(var_name)

    def get_collection(self, collection_name):
        return self.get_var(collection_name)

    def get_collection_names(self):
        return self.master.list_collection_names()

    def find(self, key, value):
        collections = self.get_collection_names()
        master_list = []
        for collection in collections:
            temp_collection = self.get_var(collection)
            raw_results = temp_collection.find({ "$or": [{key: value}, {key: int(value)}] })
            master_list += self.to_list(raw_results)
        return master_list

    """ OUT of database -> OFFICIAL DATE CONVERSION FROM DATABASE ENTRY <- """
    @staticmethod
    def from_db_date(str_date):
        date_obj = parser.parse(str_date)
        return date_obj

    """ INTO database -> OFFICIAL DATE CONVERSION FOR DATABASE ENTRY <- """
    @staticmethod
    def to_db_date(t=None):
        if t is None:
            t = datetime.datetime.now()
        date = str(t.strftime("%B")) + s + str(t.strftime("%d")) + s + str(t.strftime("%Y"))
        return date

    @staticmethod
    def parse_date(obj=None):
        if type(obj) is str:
            obj = DATE.parse_str(obj)
        elif type(obj) is list:
            return None
        p_date = str(obj.strftime("%B")) + s + str(obj.strftime("%d")) + s + str(obj.strftime("%Y"))
        return p_date

    @staticmethod
    def to_list(cursor):
        return list(cursor)

    @staticmethod
    def to_counted_dict(cursor):
        result_dict = {}
        for item in cursor:
            _id = DICT.get("_id", item)
            raw = DICT.get("raw_hookups", item)
            count = len(raw)
            result_dict[_id] = {"count": count,
                                "raw_hookups": raw}
        return result_dict

    def clean_archive_list(self, raw_hookups):
        temp_list = []
        for item in raw_hookups:
            temp_date = DICT.get("published_date", item)
            temp_body = DICT.get("body", item)
            if temp_date and temp_body:
                temp_list.append(item)
        return temp_list

    @staticmethod
    def cursor_count(cursor) -> int:
        return len(list(cursor))






