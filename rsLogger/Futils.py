import datetime

n = "\n"
s = " "
co = ", "
p = "."
c = ":"

""" INTO database -> OFFICIAL DATE CONVERSION FOR DATABASE ENTRY <- """
def to_db_date(t=None):
    if t is None:
        t = datetime.datetime.now()
    date = str(t.strftime("%B")) + s + str(t.strftime("%d")) + s + str(t.strftime("%Y"))
    return date

def get_log_date_time():
    return datetime.datetime.now()