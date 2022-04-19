from fwebUtils import DATE, DICT, Ext, Regex, Language, URL, LIST
from fwebUtils import LOGGER

isNull = lambda item: False if item and item is not None else True
safe_args = lambda *args: LIST.flatten(args)