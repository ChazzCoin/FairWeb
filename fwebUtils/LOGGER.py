import platform
import subprocess
import os
import datetime

MASTER_PATH = os.getcwd()

ERROR = 0  # -> Show ERROR only
INFO = 1  # -> Show ERROR and INFO
DEBUG = 2  # -> Show ERROR, INFO and DEBUG
VERBOSE = 3  # -> Show ERROR, INFO, DEBUG AND VERBOSE
LOG_LEVEL = DEBUG

MAC = "Darwin"
LINUX = "Linux"

OS = platform.system()


s = " "
DATETIME_MONTH = "%B"
DATETIME_DAY = "%d"
DATETIME_YEAR = "%Y"
DATETIME_REDDIT = "'%Y-%m-%d %H:%M:%S'"

def get_log_date_time_dt() -> datetime:
    return datetime.datetime.now()

def get_month_day_year_str(dtObject: datetime) -> str:
    return str(get_datetime_month(dtObject)) + s + str(get_datetime_day(dtObject)) + s + str(get_datetime_year(dtObject))

""" toString Extractors """
def get_datetime_month(datetimeObject: datetime) -> str:
    return datetimeObject.strftime(DATETIME_MONTH)

def get_datetime_day(datetimeObject: datetime) -> str:
    return datetimeObject.strftime(DATETIME_DAY)

def get_datetime_year(datetimeObject: datetime) -> str:
    return datetimeObject.strftime(DATETIME_YEAR)


class Log:
    log_level = 1
    log_color = "\33[0m"
    log_name = "FairCoreLogger"
    title = "Local-Log"
    log_path = MASTER_PATH + "/Data/Export/Logs"
    className = ""
    timeIn = 0
    timeOut = 0
    totalTime = 0

    """
    Setup:
        -> Add following two lines to any file, top of file, outside of classes.
    1. from FAIR.Logger.LocalLogger import Log
    2. Log = Log("Path.To.Python.File")

    Usage: Log.<level>(<customMessage>)
        -> success = s: Log.s("Article has successfully been downloaded!.")
        -> warning = w: Log.w("Article was downloaded with possible errors.")
        -> error = e: Log.e("Failed to Download Article.", error=e)
        -> info = i: Log.i("This is info level logging about Article")
        -> debug = d: Log.d("This is debug level logging about Article")
        -> verbose = v: Log.v("This is verbose level logging about Article")
    """

    def __init__(self, className, log_level=LOG_LEVEL, log_name="FairLogger"):
        # self.timeIn = process_time()
        # self.i("--> Run time has begun <--")
        self.log_level = log_level
        self.className = className
        self.log_name += f"{log_name}-{log_level}"

    def notify(self, text):
        """
        -> Fix this to work on Linux or macOS
        """
        if OS == MAC:
            self.v("Creating MAC Push Notification: ", text)
            os.system("""osascript -e 'display notification "{}" with title "{}"'""".format(text, self.title))
        elif OS == LINUX:
            subprocess.Popen(['notify-send', f"{self.title}: {text}"])

    def i(self, *messages, d: str = None, v: str = None):
        """ INFO Logging """
        if d:
            self.d(self.create_message(messages, d))
        if v:
            self.v(self.create_message(messages, v))
        if self.log_level == INFO:
            level = "INFO"
            self.write_log(level, self.create_message(messages))
        elif self.log_level > INFO and not d and not v:
            level = "INFO"
            self.write_log(level, self.create_message(messages))

    def e(self, *messages, error=""):
        """ ERROR Logging """
        log = f"{self.create_message(messages)}: {error}"
        level = "ERROR"
        self.write_log(level, log)

    def w(self, *messages, warning=""):
        """ WARNING Logging """
        log = f"{self.create_message(messages)}: {warning}"
        level = "WARNING"
        self.write_log(level, log)

    def d(self, *messages, v: str = None):
        """ DEBUG Logging """
        if v:
            self.v(self.create_message(messages, v))
        if self.log_level == DEBUG:
            level = "DEBUG"
            self.write_log(level, self.create_message(messages))
        elif self.log_level > DEBUG and not v:
            level = "DEBUG"
            self.write_log(level, self.create_message(messages))

    def v(self, *messages):
        """ VERBOSE Logging """
        if self.log_level >= VERBOSE:
            log = f"{self.create_message(messages)}"
            level = "VERBOSE"
            self.write_log(level, log)

    def s(self, *messages):
        """ SUCCESS Logging """
        log = f"{self.create_message(messages)}"
        level = "SUCCESS"
        self.write_log(level, log)

    def t(self, *messages):
        """ TRACE Logging """
        log = f"{self.create_message(messages)}"
        level = "TRACE"
        self.write_log(level, log)

    def p(self, *messages):
        """ Only Prints Log to Terminal/Console """
        if self.log_level >= DEBUG:
            # -> Add "p" to debug mode.
            self.d(messages)
        else:
            print(self.className, self.create_message(messages))

    def p_by_line(self, *messages):
        """ Only Prints Log to Terminal/Console """
        for message in messages:
            print(self.className, message)

    @staticmethod
    def cli(message):
        print(BOLD + f"{message}")

    def create_message(self, *messages):
        temp_message = ""
        for m in messages:
            temp_message = temp_message + " " + str(m)
        return temp_message

    def write_log(self, level, message):
        date = get_log_date_time_dt()
        log = f"{date}: {level}: {self.className} -> {message}"
        color = get_log_color(log_level=level)
        print(color + log)

    # -> Decorator
    def trace(self, msg):
        def wrapper(func):
            def runner(*args):
                self.t(f"BEGINNING: {msg}")
                func(*args)
                self.t(f"FINISHED: {msg}")

            return runner

        return wrapper



"""

-> Colors for Logging to Terminal

"""

HEADER = '\033[95m'
DEBUG_BLUE = '\033[94m'  # ->
VERBOSE_CYAN = '\033[96m'  # ->
SUCCESS_GREEN = '\033[92m'  # -> INFO
WARNING_YELLOW = '\033[93m'
ERROR_FAIL = '\033[91m'  # -> ERROR
INFO_WHITE = "\33[0m"
ENDC = '\033[0m'
BOLD = '\033[1m'
TRACE_UNDERLINE = '\033[4m'
TRACE = '\033[0;30;47m'


def get_log_color(log_level):
    if log_level == "ERROR":
        return ERROR_FAIL
    elif log_level == "WARNING":
        return WARNING_YELLOW
    elif log_level == "INFO":
        return INFO_WHITE
    elif log_level == "DEBUG":
        return DEBUG_BLUE
    elif log_level == "VERBOSE":
        return VERBOSE_CYAN
    elif log_level == "SUCCESS":
        return SUCCESS_GREEN
    elif log_level == "TRACE":
        return TRACE