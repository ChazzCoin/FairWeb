import time
from FWEB import Log, LIST
Log = Log("FWEB.Futils.Extensions")

def safe_run(func):
    def wrapper(*args):
        try:
            Log.i("Safe Running")
            return func(args)
        except Exception as e:
            Log.e("Safe Run Failed with error ->", error=e)
            return False
    return wrapper

def safe_args(func):
    def wrapper(*items) -> []:
        temp = LIST.flatten(items)
        return func(temp)
    return wrapper

# -> Pass func() into Decorator()
def safe_string(func):
    # -> Pass func args into wrapper()
    def wrapper(items) -> []:
        if type(items) not in [str]:
            return func(LIST.get(0, items))
        return func(items)
    return wrapper

# -> Pass args into Decorator()
def sleep(seconds):
    # -> Pass func() into wrapper()
    def wrapper(func):
        # -> Pass func args into runner()
        def runner(*args):
            time.sleep(seconds)
            return func(*args)
        return runner
    return wrapper