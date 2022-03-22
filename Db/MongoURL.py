from FWEB import DATE, Log, MongoCore
Log = Log("MongoURL")

class MongoURL(MongoCore):

    def get_urls(self) -> []:
        results = self.c_urls.find({"id": "8294"})
        list_of_results = self.to_list(results)
        item = list_of_results[0]
        urls = item.get("urls")
        return urls

    """ -> ADD <- """
    def add_urls(self, list_of_urls):
        count = len(list_of_urls)
        try:
            self.c_urls.insert_one({"id": "8294",
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
            self.c_urls.update_one( {"id": id},
                                   { "$set": {"date": DATE.to_db_date(),
                                              "urls": list(temp),
                                              "url_count": count, }
                                     })
            Log.s(f"update_urls: successfully added {count} urls!")
        except Exception as e:
            Log.e(f"update_urls: Failed to save {count} urls.", error=e)
            Log.notify(f"Urls failed to save.")


# if __name__ == '__main__':
#     db = MongoURL()
#     test = db.get_urls()
#     for url in test:
#         print(url)
    # db.find("urls", )
    # db.update_urls(["www.harrypotter.com", "www.gayfer.com"])