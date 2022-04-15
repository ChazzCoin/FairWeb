import json
# import pandas as pd

"""
-> "dict" object extension/helper functions
"""

def replace_key_value(dictIn, key, value):
    result = {}
    try:
        for inKey in dictIn.keys():
            if inKey == key:
                continue
            result[inKey] = dictIn[inKey]
        result[key] = value
        return result
    except Exception as e:
        print(f"Could not replace key/value pair in dict. error=[ {e} ]")
        return dictIn

def replace_in_dict(input, variables):
    result = {}
    for key, value in input.iteritems():
        if isinstance(value, dict):
            result[key] = replace_in_dict(value, variables)
        else:
            result[key] = value % variables
    return result


def get(key: str, dic, default=False):
    """
    Able to search embedded dict's for keys.
    Safely returns result or False.
    """
    try:
        # if isinstance(dic, pd.DataFrame):
        #     dic = dic.to_dict()
        if type(dic) is not dict:
            dic = dic.__dict__
        if dic.__contains__(key):
            return dic[key]
        for mainKey in dic.keys():
            tempValue = dic[mainKey]
            if mainKey == key:
                return tempValue
            if type(tempValue) is dict:
                result = get(key, tempValue)
                if not result:
                    continue
                return result
        return default
    except Exception as e:
        print("Failed to get key for dict")
        return default

def get_all(dic, *keys, force_type=None) -> []:
    """
        Find all keys in dict
        RETURNS: List[]
    """
    if force_type is True:
        force_type = [str, list, tuple, set]
    temp_list = []
    key_list = []
    first = keys[0] if len(keys) > 0 else None
    # Convert tuple(list) -> list
    if type(first) is list:
        for item in first:
            key_list.append(item)
    else:
        key_list = keys
    # -> Loop Keys to find
    for key in key_list:
        item = get(key, dic)  # -> Deep Get ^ on dict
        itemType = type(item)
        # if null
        if item is None or item is False:
            continue
        if force_type:
            if itemType in force_type:
                temp_list.append(item)
            else:
                continue
        # if list, set, or tuple
        elif itemType in [list, set, tuple]:
            for i in item:
                temp_list.append(i)
        # if dict
        elif itemType is dict:
            list_of_items = to_value_list(item)
            for i in list_of_items:
                temp_list.append(i)
        else:
            temp_list.append(item)
    # -> Post Work
    if len(temp_list) == 1:
        final_result = temp_list[0]
    else:
        final_result = temp_list
    return final_result

def merge_dicts(*dict_args):
    """
    -> LAZY MERGING
    Given any number of dictionaries, shallow copy and merge into a new dict,
    precedence goes to key-value pairs in latter dictionaries.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

# -> Takes word count dicts and add the values into one count.
def add(*dicts) -> dict:
    """ Add two dicts of word counts together """
    result = {}
    # -> Loop each dictionary
    for dictionary in dicts:
        # Loop each key
        for key in dictionary.main_category_keys():
            if result.__contains__(key):
                temp = result[key] + dictionary[key]
                result[key] = temp
            else:
                result[key] = dictionary[key]
    return result

def add_merge_count_to_value(temp: dict, result: dict) -> dict:
    """ -> DEPRECATED <- by "add" Adds value count, merging dicts together """
    for key in result.keys():
        count = result[key]
        if key in temp.keys():
            temp[key] += count
        else:
            temp[key] = count
    return temp

if __name__ == '__main__':
    one = { "word1": 1, "word2": 4, "word4": 3, "word5": 19 }
    two = {"word1": 1, "word2": 1, "word4": 1, "word0": 0}
    print(add_merge_count_to_value(one, two))

def count_list_of_words(words):
    result = {}
    for item in words:
        result = add_matched_word_to_result(item, result)
    return result

def add_matched_word_to_result(word: str, dic: dict) -> dict:
    if word in dic.keys():
        dic[word] += 1
    else:
        dic[word] = 1
    return dic

# -> Handles NLTK Single, Bi, Tri and Quad Terms
def convert_tuples_to_dict(list_of_tuples: [()]) -> dict:
    unique_list = list(set(list_of_tuples))
    temp_dict = {}
    for master_item in unique_list:
        if type(master_item[0]) is tuple:
            joined_tuple = " ".join(master_item[0])
            score = master_item[1]
            temp_dict[joined_tuple] = score
        elif type(master_item[0]) is str:
            word = master_item[0]
            score = master_item[1]
            temp_dict[word] = score
    return temp_dict


def remove_duplicates(key, dic: dict) -> list:
    unique = { each[key]: each for each in dic }.values()
    result = []
    for key in unique:
        result.append(key)
    return result

def removeKeyValue(key, dic: dict) -> dict:
    try:
        del dic[key]
        return dic
    except Exception as e:
        print("Failed to delete key value")
        return dic

def addKeyValue(key, value, dic: dict, forceList=False) -> dict:
    if dic.__contains__(key):
        temp = dic[key]
        if type(temp) in [list, tuple]:
            temp.append(value)
        elif type(temp) is str:
            temp = temp + value
        elif type(temp) is int:
            temp += value
        else:
            new = [temp, value]
            temp = new
        dic[key] = temp
    else:
        if forceList:
            dic[key] = [value]
        else:
            dic[key] = value
    return dic

def hookups_are_identical(hookup1, hookup2) -> bool:
    count = 0
    tempBody1 = get("body", hookup1)
    tempTitle1 = get("title", hookup1)
    tempUrl1 = get("url", hookup1)
    tempBody2 = get("body", hookup2)
    tempTitle2 = get("title", hookup2)
    tempUrl2 = get("url", hookup2)
    if tempTitle1 == tempTitle2:
        count += 1
    if tempBody1 == tempBody2:
        count += 1
    if tempUrl1 == tempUrl2:
        count += 1
    if count >= 2:
        return True
    else:
        return False

def categorize_hookups(hookups):
    if not hookups:
        return False
    categories = {}
    for hookup in hookups:
        cat = get("category", hookup)
        categories = addKeyValue(cat, hookup, categories, forceList=True)
    return categories


def to_value_list(data: dict) -> list:
    temp_list = []
    for key in data.keys():
        temp_list.append(data[key])
    return temp_list

def to_key_list(data: dict) -> list:
    temp_list = []
    for key in data.keys():
        temp_list.append(key)
    return temp_list

def to_pretty_json(data: dict, indent=4):
    obj = json.dumps(data, sort_keys=True, indent=indent, default=str)
    return obj

def order_by_value(dic: dict) -> dict:
    return {k: v for k, v in sorted(dic.items(), key=lambda item: item[1], reverse=True)}



