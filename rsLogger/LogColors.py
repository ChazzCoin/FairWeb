

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