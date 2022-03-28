from FWEB.Futils import DATE
from FWEB.Db.MongoCore import MongoCore
from FWEB.rsLogger import Log
Log = Log("MongoURL")

class MongoURL(MongoCore):

    def get_urls(self) -> []:
        results = self.c_sources.find({"source": "urls"})
        list_of_results = self.to_list(results)
        item = list_of_results[0]
        urls = item.get("list")
        return urls

    """ -> ADD <- """
    def add_urls(self, list_of_urls):
        count = len(list_of_urls)
        try:
            self.c_sources.insert_one({"id": "8294",
                                        "date": DATE.to_db_date(),
                                        "urls": list_of_urls,
                                        "url_count": count, })
            Log.s(f"add_urls: successfully added {count} urls!")
        except Exception as e:
            Log.e(f"add_urls: Failed to save {count} urls.", error=e)
            Log.notify(f"Urls failed to save.")

    def update_urls(self, list_of_urls, id="8294"):
        count = len(list_of_urls)
        temp = set(self.get_urls() + list_of_urls)
        try:
            self.c_sources.update_one({"id": id},
                                      { "$set": {"date": DATE.to_db_date(),
                                              "urls": list(temp),
                                              "url_count": count, }
                                     })
            Log.s(f"update_urls: successfully added {count} urls!")
        except Exception as e:
            Log.e(f"update_urls: Failed to save {count} urls.", error=e)
            Log.notify(f"Urls failed to save.")
