from FWEB import DICT, DATE, Log
from FWEB.Parser import Keys
Log = Log("FWEB.Parser.JsonParser")

""" import keys() method from Keys Module. """
keys = Keys.keys

def parse(data, parseAll=False) -> {}:
    Log.d("Parsing data IN", v=f"=[ {data} ]")
    try:
        json_obj = {}
        json_obj["author"] = DICT.get_all(data, keys("author"), force_type=True)
        json_obj["title"] = DICT.get_all(data, keys("title"), force_type=True)
        json_obj["description"] = DICT.get_all(data, keys("description"), force_type=True)
        json_obj["body"] = DICT.get_all(data, keys("body"), force_type=True)
        json_obj["url"] = DICT.get_all(data, keys("url"), force_type=True)
        json_obj["img_url"] = DICT.get_all(data, keys("imgUrl"), force_type=True)
        json_obj["source"] = DICT.get_all(data, keys("source_url"), force_type=True)
        json_obj["tickers"] = DICT.get_all(data, keys("tickers"))
        json_obj["tags"] = DICT.get_all(data, keys("tags"))
        temp_date = DICT.get_all(data, keys("published_date"))
        json_obj["published_date"] = DATE.parse(temp_date)

        if parseAll:
            json_obj["summary"] = DICT.get("summary", data)
            json_obj["comments"] = DICT.get("comments", data)
            json_obj["source_rank"] = DICT.get("source_rank", data)
            json_obj["category"] = DICT.get("category", data)
            json_obj["sentiment"] = DICT.get("sentiment", data)
            json_obj["category_scores"] = DICT.get("category_scores", data)
            json_obj["score"] = DICT.get("score", data)
            json_obj["title_score"] = DICT.get("title_score", data)
            json_obj["description_score"] = DICT.get("description_score", data)
            json_obj["body_score"] = DICT.get("body_score", data)

        Log.v(f"Parsing data OUT=[ {json_obj} ]")
        return json_obj
    except Exception as e:
        Log.e(f"Failed to parse data=[ {data} ]", e)
        return None