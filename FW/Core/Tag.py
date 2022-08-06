from bs4.element import Tag as bsTag
from F import DICT
from F import LIST
from FNLP.Regex import Re as Regex
from F.LOG import Log
Log = Log("FWEB.Tag")
import sys

sys.setrecursionlimit(10000)

"""
        1. Element -> holds Tag(s)
        2. Tag(s) -> are Nodes with a "next_element" that is another Tag(s).
        2. Tag(s) -> have key/value pairs.
        4. Tag(s) -> have "attrs" that is a dict of "attributes".

        Element = { Tag(s)? }
        Tag = { name, text, attrs?, next_element?/Tag? }
    """
def search(master_element, terms, enableName=True, enableText=True, enableAttributes=True):
    """ -> Master Search, Handles both Elements or Tags. <- """
    if not master_element:
        return False
    if not is_tag(master_element):
        # Element
        return search_element(master_element, terms, enableName=enableName, enableText=enableText, enableAttributes=enableAttributes)
    else:
        # Tag
        return search_tag_deep(master_element, terms,
                                 enableName=enableName, enableText=enableText, enableAttributes=enableAttributes)
def search_element(master_element, terms, enableName=False, enableText=False, enableAttributes=False):
    if not master_element:
        return False
    for tag in master_element:
        temp = find(tag, terms,
                        enableName=enableName, enableText=enableText, enableAttributes=enableAttributes)
        if temp:
            return temp
        result = search_tag_deep(tag, terms,
                                 enableName=enableName, enableText=enableText, enableAttributes=enableAttributes)
        if result:
            return result
    return False

def search_tag_deep(master_tag: bsTag, terms, enableName=False, enableText=False, enableAttributes=False):
    """ -> Loops All Elements in Tag, then Recursively Loops each Tag <- """
    if not master_tag:
        return False
    if not is_tag(master_tag):
        return False
    try:
        temp = find(master_tag, terms,
                        enableName=enableName, enableText=enableText, enableAttributes=enableAttributes)
        if temp:
            return temp
        tempMaster = search_tag(master_tag, terms,
                              enableName=enableName, enableText=enableText, enableAttributes=enableAttributes)
        if tempMaster:
            return tempMaster
        all_tags = master_tag.find_all_next()
        if all_tags:
            for subTag in all_tags:
                if subTag and subTag != "\n" and subTag != "" and subTag != " ":
                    temp = search_tag(subTag, terms,
                                        enableName=enableName, enableText=enableText, enableAttributes=enableAttributes)
                    if temp:
                        return temp
        Log.v(f" -> find_tag() found nothing for TERMS=[ {terms} ].")
        return False
    except Exception as e:
        Log.e(" -> find_tag() has failed.", error=e)
        return False

def search_tag(master_tag: bsTag, terms, enableName=True, enableText=True, enableAttributes=True):
    """ -> A Recursive Loop through each "next_element"/Tag <- """
    if not is_tag(master_tag):
        return False
    try:
        Log.d(f"Searching... [ {master_tag.name} ]")
        # -> Search Tag
        result = find(master_tag, terms,
                          enableName=enableName, enableText=enableText, enableAttributes=enableAttributes)
        if result:
            return result
        else:
            next_tag = master_tag.next_element
            if next_tag and next_tag != "\n" and next_tag != "" and next_tag != " ":
                return search_tag(next_tag, terms,
                                      enableName=enableName, enableText=enableText, enableAttributes=enableAttributes)
    except Exception as e:
        Log.e("Something went wrong during tag search.", error=e)
        return False

""" Next Layer """
def find(master_tag, terms, enableName, enableText, enableAttributes):
    """ -> Searches the single current  <- """
    Log.v(f" -> find() {terms}.")
    if not is_tag(master_tag):
        return False
    # -> Search Name
    if enableName:
        tagTemp = search_name(master_tag, terms)
        if tagTemp:
            return tagTemp
    # -> Search Text
    if enableText:
        text = search_text(master_tag, terms)
        if text:
            return text
    # -> Search Attributes
    if enableAttributes:
        attributes = search_attributes(master_tag, terms)
        if attributes:
            return attributes
        return False

def is_tag(master_tag):
    if not master_tag:
        Log.v(" -> search_tag() master_tag is Empty.")
        return False
    if not isinstance(master_tag, bsTag):
        Log.v(" -> search_tag() master_tag is not a [bsTag].")
        return False
    return True

def search_name(master_tag, terms):
    """ -> CORE SEARCH OF TAG NAME <- """
    if not is_tag(master_tag):
        return False
    tagName = master_tag.name
    tagTemp = Regex.contains_any(terms, content=tagName)
    if tagTemp:
        return "name", tagName, master_tag
    return False

def search_attributes(master_tag, terms):
    """ -> CORE SEARCH OF TAG ATTRIBUTES <- """
    if not is_tag(master_tag):
        return False
    try:
        attributes = DICT.get("attrs", master_tag)
        if attributes:
            for key in attributes.keys():
                value = DICT.get(key, attributes)
                kTemp = Regex.contains_any(terms, content=key)
                if kTemp:
                    Log.d(f" -> find() Key Found. KEY=[ {key} ].")
                    print("Key Found.", key)
                    return key, value, master_tag
                vTemp = Regex.contains_any(terms, content=value)
                if vTemp:
                    Log.d(f" -> find() Value Found. VALUE=[ {value} ].")
                    return key, value, master_tag
        return False
    except Exception as e:
        Log.e("Finding Attribute ", error=e)
        return False

def get_attribute(master_tag, key):
    """ -> CORE SEARCH OF TAG ATTRIBUTES <- """
    if not is_tag(master_tag):
        return False
    attributes = DICT.get("attrs", master_tag)
    if attributes:
        value = DICT.get(key, attributes)
        return value
    return False

def search_text(master_tag, terms):
    """ -> CORE SEARCH OF TAG TEXT <- """
    if not is_tag(master_tag):
        return False
    test = master_tag.text
    if test != "":
        tTemp = Regex.contains_any(terms, content=test)
        if tTemp:
            Log.d(f" -> find() Text Found. TEXT=[ {test} ].")
            return "text", master_tag.text, master_tag
    return False

def get_text(master_tag):
    """ -> CORE GET OF TAG TEXT <- """
    if not is_tag(master_tag):
        return False
    test = master_tag.text
    if test != "":
        Log.d(f" -> find() Text Found. TEXT=[ {test} ].")
        return master_tag.text
    return False

def get_value_for_key(master_tag, key):
    if not is_tag(master_tag):
        return False
    results = get_attribute(master_tag, key)
    if results:
        return results
    return False

def search_key(master_tag, terms):
    if not is_tag(master_tag):
        return False
    results = search_tag_deep(master_tag, terms, enableAttributes=True)
    if results:
        return LIST.get(0, results)
    return False

def search_value(master_tag, terms):
    if not is_tag(master_tag):
        return False
    results = search_tag_deep(master_tag, terms, enableAttributes=True)
    if results:
        return LIST.get(1, results)
    return False

def search_tag_name(master_tag, terms):
    if not is_tag(master_tag):
        return False
    results = search_tag_deep(master_tag, terms, enableName=True)
    if results:
        return results[2]
    return False

def contains_attribute(*attributes, tag):
    if not is_tag(tag):
        return False
    attributes = LIST.flatten(attributes)
    for attribute in attributes:
        if tag.has_attr(attribute):
            return attribute
    return False