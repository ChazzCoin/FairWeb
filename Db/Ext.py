from FWEB.Db import MongoURL

def injectUrls(func):
    def runner():
        urls = MongoURL().get_urls()
        return func(urls)
    return runner