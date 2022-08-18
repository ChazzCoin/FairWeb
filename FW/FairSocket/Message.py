import F
from F import DATE
from F.CLASS import FairClass

class FairMessage(FairClass):
    messageId = F.get_uuid()
    date = DATE.get_now_month_day_year_str()
    userName = ""
    sender = ""
    fromEventName = "onMessage"
    receiver = ""
    toEventName = "onMessage"
    message = ""
    action = ""
