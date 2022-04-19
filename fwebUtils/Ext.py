import sys
import threading
import time
from fwebUtils import LIST
from fwebUtils.LOGGER import Log
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

def safe_run_return(default=False):
    def wrapper(func):
        def runner(*args):
            try:
                Log.i("Safe Running")
                return func(args)
            except Exception as e:
                Log.e("Safe Run Failed with error ->", error=e)
                return default
        return runner
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

def timelimit(timeout):
    """Borrowed from web.py, rip Aaron Swartz
    """
    def _1(function):
        def _2(*args, **kw):
            class Dispatch(threading.Thread):
                def __init__(self):
                    threading.Thread.__init__(self)
                    self.result = None
                    self.error = None

                    self.setDaemon(True)
                    self.start()

                def run(self):
                    try:
                        self.result = function(*args, **kw)
                    except:
                        self.error = sys.exc_info()
            c = Dispatch()
            c.join(timeout)
            if not c.result:
                raise TimeoutError()
                # return False
            if c.error:
                raise c.error[0](c.error[1])
                # return False
            return c.result
        return _2
    return _1

def print_duration(method):
    """Prints out the runtime duration of a method in seconds
    """
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('%r %2.2f sec' % (method.__name__, te - ts))
        return result
    return timed