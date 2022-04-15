import datetime
import time
from dateutil import parser
import dateutil.relativedelta

from fwebUtils import Regex, LIST

n = "\n"
s = " "
co = ", "
p = "."
c = ":"

""" OUT of database -> OFFICIAL DATE CONVERSION FROM DATABASE ENTRY <- """
def from_db_date(str_date):
    date_obj = parser.parse(str_date)
    return date_obj


""" INTO database -> OFFICIAL DATE CONVERSION FOR DATABASE ENTRY <- """
def to_db_date(t=None):
    if t is None:
        t = datetime.datetime.now()
    date = str(t.strftime("%B")) + s + str(t.strftime("%d")) + s + str(t.strftime("%Y"))
    return date

def parse(obj=None):
    try:
        if type(obj) is str:
            obj = parse_str(obj)
        elif type(obj) is list:
            return None
        p_date = str(obj.strftime("%B")) + s + str(obj.strftime("%d")) + s + str(obj.strftime("%Y"))
        return p_date
    except Exception as e:
        print(f"Failed to parse obj to date: [ {obj} ]", e)
        return None

def convert_reddit_to_datetime(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


def sort_jarticles_by_date(list_of_jarticles) -> dict:
    try:
        from Utils import DICT
        by_date = {}
        for jarticle in list_of_jarticles:
            temp_date = DICT.get("published_date", jarticle)
            if by_date.__contains__(temp_date):
                temp_list = by_date[temp_date]
                temp_list.append(jarticle)
                by_date[temp_date] = temp_list
            else:
                by_date[temp_date] = [jarticle]
        return by_date
    except Exception as e:
        print("Failed to sort hookups by date.", e)
        return list_of_jarticles

# def get_date_for_db(t=None):
#     if t is None:
#         t = datetime.datetime.now()
#     date = str(t.strftime("%A")) + p + str(t.strftime("%B")) + p + str(t.strftime("%d")) + p + str(t.strftime("%Y"))
#     return date


def get_timestamp():
    return str(time.time())

def get_log_date_time():
    return datetime.datetime.now()

# Get Now
def get_now_date():
    return datetime.datetime.now().date()

def build_date(day, month, year):
    return datetime.datetime(year, month, day).date()

def build_date_for_db(day, month, year):
    return to_db_date(datetime.datetime(year, month, day))

# -> Master Parser
def parse_str(obj: str):
    return parser.parse(obj)

# # -> Subtract Days
# def subtract_days(date: datetime, days=1):
#     days = datetime.timedelta(days)
#     new_date = date - days
#     return new_date

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

def mongo_date_today():
    obj = get_now_date()
    p_date = str(obj.strftime("%B")) + s + str(obj.strftime("%d")) + s + str(obj.strftime("%Y"))
    return p_date

def get_current_year():
    obj = get_now_date()
    return str(obj.strftime("%Y"))

def get_current_month():
    obj = get_now_date()
    return str(obj.strftime("%B"))

def get_current_day():
    obj = get_now_date()
    return str(obj.strftime("%d"))

def get_last_seven_days():
    return get_last_x_days(6)

def get_last_thirty_days():
    return get_last_x_days(30)



def to_hours_minutes_seconds(seconds):
    return str(datetime.timedelta(seconds=seconds))

def add_months(str_date, months=1):
    date = parser.parse(str_date)
    newDate = date + dateutil.relativedelta.relativedelta(months=months)
    return to_db_date(newDate)

def subtract_months(str_date, months=1):
    date = parser.parse(str_date)
    newDate = date - dateutil.relativedelta.relativedelta(months=months)
    return to_db_date(newDate)

def subtract_years(str_date, years=1):
    date = parser.parse(str_date)
    newDate = date - dateutil.relativedelta.relativedelta(years=years)
    return to_db_date(newDate)

def subtract_hours(str_date, hours=1):
    date = parser.parse(str_date)
    newDate = date - dateutil.relativedelta.relativedelta(hours=hours)
    return to_db_date(newDate)

def subtract_days(str_date, days=1):
    date = parser.parse(str_date)
    newDate = date - dateutil.relativedelta.relativedelta(days=days)
    return to_db_date(newDate)

def get_range_of_dates(startDate, daysBack=1):
    current_date = startDate
    list_of_dates = [startDate]
    for i in range(daysBack):
        current_date = subtract_days(current_date, 1)
        list_of_dates.append(current_date)
    return list_of_dates

def parse_reddit_timestamp(timestamp):
    """
    -> Converts '11 hours ago' -> 'Month Day Year'
    :param timestamp: '2 months ago'
    :return: 'Month Day Year' from current date.
    """
    count = [int(s) for s in timestamp.split() if s.isdigit()]
    if not count:
        count = 0
    else:
        count = LIST.get(0, count)
    if Regex.contains_any(["min", "minute", "minutes"], timestamp):
        return parse_date(get_now_date())
    if Regex.contains_any(["hours", "hour", "min", "minute", "minutes"], timestamp):
        return subtract_hours(parse_date(get_now_date()), count)
    if Regex.contains_any(["day", "days"], timestamp):
        return subtract_days(parse_date(get_now_date()), count)
    if Regex.contains_any(["month", "months"], timestamp):
        return subtract_months(parse_date(get_now_date()), count)
    if Regex.contains_any(["year", "years"], timestamp):
        return subtract_years(parse_date(get_now_date()), count)
    return timestamp

def get_last_x_days(days):
    if days == 1:
        return [parse_date(get_now_date())]
    i = days - 1
    temp = []
    now = get_now_date()
    today_date = parse_date(now)
    temp.append(today_date)
    while i > 0:
        minus_one = subtract_days(now)
        minus_one_date = parse_date(minus_one)
        now = minus_one
        temp.append(minus_one_date)
        i -= 1
    return temp

if __name__ == '__main__':
    parse_reddit_timestamp("8 months ago")

months = {
    "January": ["January", "Jan"],
    "February": ["February", "Feb"],
    "March": ["March", "Mar"],
    "April": ["April", "Apr"],
    "May": ["May"],
    "June": ["June", "Jun"],
    "July": ["July", "Jul"],
    "August": ["August", "Aug"],
    "September": ["September", "Sept", "Sep"],
    "October": ["October", "Oct"],
    "November": ["November", "Nov"],
    "December": ["December", "Dec"]
}

days = {
    "Monday": ["Monday", "Mon"],
    "Tuesday": ["Tuesday", "Tues"],
    "Wednesday": ["Wednesday", "Wed"],
    "Thursday": ["Thursday", "Thur", "Thurs"],
    "Friday": ["Friday", "Fri"],
    "Saturday": ["Saturday", "Sat"],
    "Sunday": ["Sunday", "Sun"]
}