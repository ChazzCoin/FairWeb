from FWEB.rsLogger import Futils, LogColors, fig
import os


class Log:
    log_level = 1
    log_color = "\33[0m"
    log_name = "FairLocalLogger"
    title = "Local-Log"
    log_path = fig.MASTER_PATH + "/Data/Export/Logs"
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

    def __init__(self, className, log_level=fig.LOG_LEVEL, log_name="FairLogger"):
        # self.timeIn = process_time()
        # self.i("--> Run time has begun <--")
        self.log_level = log_level
        self.className = className
        self.log_name += f"{log_name}-{log_level}-{Futils.to_db_date()}"

    def notify(self, text):
        """
        -> Fix this to work on Linux or macOS
        """
        self.v("Creating MAC Push Notification: ", text)
        os.system("""osascript -e 'display notification "{}" with title "{}"'""".format(text, self.title))

    def i(self, *messages, d: str = None, v: str = None):
        """ INFO Logging """
        if d:
            self.d(self.create_message(messages, d))
        if v:
            self.v(self.create_message(messages, v))
        if self.log_level == fig.INFO:
            level = "INFO"
            self.write_log(level, self.create_message(messages))
        elif self.log_level > fig.INFO and not d and not v:
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
        if self.log_level == fig.DEBUG:
            level = "DEBUG"
            self.write_log(level, self.create_message(messages))
        elif self.log_level > fig.DEBUG and not v:
            level = "DEBUG"
            self.write_log(level, self.create_message(messages))

    def v(self, *messages):
        """ VERBOSE Logging """
        if self.log_level >= fig.VERBOSE:
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
        if self.log_level >= fig.DEBUG:
            # -> Add "p" to debug mode.
            self.d(messages)
        else:
            print(self.className, self.create_message(messages))

    def p_by_line(self, *messages):
        """ Only Prints Log to Terminal/Console """
        for message in messages:
            print(self.className, message)

    def print_hookups(self, hookups):
        for item in hookups:
            self.print_hookup(item)

    def print_hookup(self, hookup):
        from Utils import DICT
        self.p("-- -- -- --")
        self.p(f"Title:", str(DICT.get("title", hookup)))
        self.p(f"Rank:", str(DICT.get("rank", hookup)))
        self.p(f"URL:", str(DICT.get("url", hookup)))
        self.p("-- -- -- --")

    def create_message(self, *messages):
        temp_message = ""
        for m in messages:
            temp_message = temp_message + " " + str(m)
        return temp_message

    def write_log(self, level, message):
        date = Futils.get_log_date_time()
        log = f"{date}: {level}: {self.className} -> {message}"
        color = LogColors.get_log_color(log_level=level)
        print(color + log)
        # self.write_log_file(log)

    def write_log_file(self, log):
        log_file = self.open_log_file()
        log_file.write(log)
        log_file.write("\n")
        log_file.close()

    def open_log_file(self):
        log_file = open(f'{self.log_path}/{self.log_name}.log', 'a')
        return log_file

    # -> Decorator
    def trace(self, msg):
        def wrapper(func):
            def runner(*args):
                self.t(f"BEGINNING: {msg}")
                func(*args)
                self.t(f"FINISHED: {msg}")
            return runner
        return wrapper
