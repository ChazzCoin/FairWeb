from FWEB.Futils import DATE, DICT
from FWEB.rsLogger import Log
from FWEB.Db.MongoArchive import MongoArchive
Log = Log("FWEB.Core.Validator")

def validateAndSave(article: {}, saveToArchive=False, setDateToToday=False) -> bool:
    date = DICT.get("published_date", article)
    body = DICT.get("body", article)
    if not date and setDateToToday and body and not body.startswith("Something went wrong"):
        date = DATE.mongo_date_today()
        article["published_date"] = date
    if date and not body.startswith("Something went wrong"):
        Log.s(f"Article Validated. Saving Now. DATE=[ {date} ]")
        if saveToArchive:
            save_article(article)
            return True
    else:
        Log.w("Failed to Validate Article.", warning=f"DATE=[ {date} ]")
        return False

def validate_article(article):
    date = DICT.get("published_date", article)
    body = DICT.get("body", article)
    if date and not body.startswith("Something went wrong"):
        Log.s(f"Article Validated. DATE=[ {date} ]")
        return True
    else:
        Log.w("Failed to Validate Article.", warning=f"DATE=[ {date} ]")
        return False

def save_article(article):
    db = MongoArchive()
    db.addUpdate_archives(article)
    return True

def mongo_save(func):
    """ -> DECORATOR <- """
    def wrapper(*args):
        # -> func() should return Article in JSON format.
        temp = func(*args)
        if temp and validate_article(temp):
            Log.i("ARTICLE HAS BEEN WRAPPED AND VALIDATED!")
            from Mongodb.MongoArchive import MongoArchive
            db = MongoArchive()
            db.addUpdate_archives(temp)
            return True
        return False
    return wrapper