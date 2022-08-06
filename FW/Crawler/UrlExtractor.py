from F import LIST
from F import DICT
from F.LOG import Log
from FNLP import URL
from FNLP.Regex import Re as Regex
Log = Log("FairWEB.Crawler.UrlExtractor")

way_back_machine_url = "https://web.archive.org"

def extract_urls_from_soup(soup, masterUrl, stayWithin=None):
    try:
        if not soup:
            return False
        Log.v("Extracting URLs via Soup.")
        soup_urls = soup.findAll('a', href=True)
        fair_urls = URL.find_urls_in_str(soup.__str__())
        extracted_urls = LIST.flatten(soup_urls, fair_urls)
        # -> Add all URLs to Queue
        full_list = private_clean_extracted_urls(masterUrl, extracted_urls)
        if stayWithin:
            filtered_list = private_filter_out_from_stayWithin(full_list, stayWithin)
            return filtered_list
        return full_list
    except Exception as e:
        Log.e("Failed to extract Urls.", error=e)
        return False


def private_clean_extracted_urls(masterUrl, extracted_urls):
    """
    -> Takes raw urls and extensions and combines them
    :param masterUrl:
    :param extracted_urls:
    :return:
    """
    if not extracted_urls:
        Log.i("No Extracted URLS")
        return
    Log.i("Looping extracted urls.")
    cleaned_urls = []
    try:
        for item in extracted_urls:
            _url = DICT.get("href", item)
            Log.d(f"Looking at URL= [ {_url} ]")
            # Web Archive Site
            if str(_url).startswith("/web/") and _url:
                Log.i(f"Url is in way back machine. Fixing url.. [ {_url} ].")
                _url = str(way_back_machine_url) + str(_url)
            # If url begins with / then it's an ext.
            if str(_url).startswith("/"):
                _url = f"https://{masterUrl}{str(_url)}"
            if str(_url).startswith("//"):
                _url = f"https://www.{str(_url)}"
            if _url and str(_url).startswith("http"):
                cleaned_urls.append(_url)
                continue
        return cleaned_urls
    except Exception as e:
        Log.e(f"Failed to handle URLs. Continuing... error=[ {e} ]")
        return extracted_urls

def private_filter_out_from_stayWithin(url_list, stayWithin):
    try:
        filtered_list = []
        for _url in url_list:
            base_url = URL.get_base_url(_url)
            if Regex.contains(stayWithin, base_url):
                filtered_list.append(_url)
            else:
                Log.v(f"Not inside staywithin [ {_url} ]")
                continue
        return filtered_list
    except Exception as e:
        Log.e("Failed to filter URL's.", error=e)
        return url_list