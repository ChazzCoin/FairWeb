import re
from fwebUtils import DATE, LIST
from fwebUtils.LOGGER import Log
Log = Log("FWEB.Futils.Regex")

def remove_special_characters(text):
    """ DEPRECATED """
    newText = re.sub('[^a-zA-Z0-9]', ' ', text)
    return newText

def search(search_term, content):
    match = re.findall(fr'.*{search_term}.*', content)
    return match if len(match) >= 1 and match is not None else False

def contains(search_term, content):
    try:
        if type(content) in [list, tuple]:
            for itemContent in content:
                match = re.findall(fr'.*{search_term}.*', itemContent)
                if len(match) >= 1 and match is not None:
                    return True
            return False
        else:
            match = re.findall(fr'.*{search_term}.*', content)
            return True if len(match) >= 1 and match is not None else False
    except Exception as e:
        Log.e(f"Failed to regex findall. {search_term}", error=e)
        return False

def contains_any(search_terms, content):
    search_terms = LIST.flatten(search_terms)
    for term in search_terms:
        temp = contains(str(term), content)
        if temp:
            return True
    return False

def str_contains_year(content):
    match = re.findall(r'\b[1-2][0-9][0-9][0-9]\b', content)
    if match and len(match) >= 1:
        if LIST.get(0, match) == "":
            return False

        newMatch = []
        for year in match:
            if len(year) > 4:
                continue
            if int(year) > int(DATE.get_current_year()):
                continue
            if int(year) < 1900:
                continue

            newMatch.append(year)
        return newMatch

def locate_term_in_str(term, content):
    match = re.search(fr'\b{term}\b', content)
    if match:
        return match
    return False


"""
1. March 02 2022
2. 03/02/2022
3. 03-02-2022
4. 2022-03-02
"""
def extract_date(content):
    if type(content) not in [str]:
        content = str(content)
    all = []
    months = DATE.months.main_category_keys()
    for item in months:
        all.append(item)
    month_variants = DATE.months.values()
    for item in month_variants:
        all.append(item)
    temp_all = LIST.flatten(all)
    _all = LIST.remove_dups(temp_all)
    for month_variant in _all:
        # -> Check for any Month or Month Variant in Full String
        locate_month_variant = locate_term_in_str(month_variant, content)
        if locate_month_variant:
            start = locate_month_variant.start()
            end = start + 15
            temp = content[start:end]
            # -> Check for Year immediately after Month
            find_year = str_contains_year(temp)
            year = LIST.get(0, find_year)
            locate_year = locate_term_in_str(year, temp)
            if locate_year:
                year_end = locate_year.end()
                temp2 = content[start:start+year_end]
                # -> Clean Result.
                filter = remove_special_characters(temp2)
                result = filter.replace("  ", " ").strip()
                return result
    return False