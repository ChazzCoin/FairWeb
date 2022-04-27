from FSON import DICT
from FDate import DATE
from FLog.LOGGER import Log
from Jarticle.jArticles import jArticles
Log = Log("FWEB.Core.Validator")


def validateAndSave(article: {}, saveToArchive=False, setDateToToday=False) -> bool:
    date = DICT.get("published_date", article)
    body = DICT.get("body", article)
    if not date and setDateToToday and body and not body.startswith("Something went wrong"):
        date = DATE.get_now_month_day_year_str()
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
    return jArticles.ADD_ARTICLES(article)

def mongo_save(func):
    """ -> DECORATOR <- """
    def wrapper(*args):
        # -> func() should return Article in JSON format.
        temp = func(*args)
        if temp and validate_article(temp):
            Log.i("ARTICLE HAS BEEN WRAPPED AND VALIDATED!")
            jArticles.ADD_ARTICLES(temp)
            return True
        return False
    return wrapper