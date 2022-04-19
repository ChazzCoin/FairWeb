from fwebUtils import DICT, DATE
from fwebUtils.LOGGER import Log
from fwebParser import Keys

Log = Log("FWEB.Parser.JsonParser")

""" import keys() method from Keys Module. """
keys = Keys.keys


def parse(data, parseAll=False, client=False) -> {}:
    Log.d("Parsing data IN", v=f"=[ {data} ]")
    try:
        json_obj = {}
        # Core All
        json_obj["author"] = DICT.get_all(data, keys("author"), force_type=True)
        json_obj["title"] = DICT.get_all(data, keys("title"), force_type=True)
        json_obj["body"] = DICT.get_all(data, keys("body"), force_type=True)
        json_obj["url"] = DICT.get_all(data, keys("url"), force_type=True)
        json_obj["source_url"] = DICT.get_all(data, keys("source_url"), force_type=True)
        json_obj["client"] = client
        temp_date = DICT.get_all(data, keys("published_date"))
        json_obj["published_date"] = DATE.parse(temp_date)
        json_obj["date_created"] = DATE.parse_date(DATE.get_now_date())
        # + Article Core
        json_obj["description"] = DICT.get_all(data, keys("description"), force_type=True)
        json_obj["img_url"] = DICT.get_all(data, keys("imgUrl"), force_type=True)
        # enhanced -> Jarticle
        if parseAll:
            json_obj["tickers"] = DICT.get_all(data, keys("tickers"))
            json_obj["tags"] = DICT.get_all(data, keys("tags"))
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


def parse_from_reddit_client(raw_post, subreddit):
    json_objc = {}
    author = DICT.get("author", raw_post)
    # Core
    json_objc["author"] = DICT.get("name", author)
    json_objc["title"] = DICT.get("title", raw_post)
    json_objc["body"] = DICT.get("selftext", raw_post, default="Post-Body-Empty")
    json_objc["url"] = DICT.get("url", raw_post)
    dt = DATE.convert_reddit_to_datetime(DICT.get("created_utc", raw_post))
    json_objc["published_date"] = DATE.parse(dt)
    json_objc["date_created"] = DATE.parse_date(DATE.get_now_date())
    json_objc["client"] = "reddit client"
    json_objc["source"] = "reddit"
    json_objc["source_url"] = "www.reddit.com"
    # + Reddit Core
    json_objc["subreddit"] = f"r/{subreddit}"
    json_objc["up_votes"] = DICT.get("ups", raw_post)
    json_objc["upvote_ratio"] = DICT.get("upvote_ratio", raw_post)
    json_objc["post_score"] = DICT.get("score", raw_post)
    json_objc["comments"] = parse_comments_into_json_list(raw_post.comments)
    json_objc["comment_count"] = DICT.get("num_comments", raw_post)
    return json_objc


def parse_comments_into_json_list(comments):
    temp_list = []
    for comment in comments:
        if len(temp_list) > 200:
            continue
        try:
            user_name = comment.author.name
            if user_name == "AutoModerator":
                continue
        except Exception as e:
            Log.d("No User for Comment", e)
            continue
        dt = DATE.convert_reddit_to_datetime(comment.created_utc)
        temp_json = {
            "author": user_name,
            "body": comment.body,
            "up_votes": comment.ups,
            "published_date": DATE.parse(dt)
        }
        temp_list.append(temp_json)
    return temp_list

def parse_from_twitter_client(raw_tweet):
    json_objc = {}
    # Core
    json_objc["author"] = DICT.get("name", raw_tweet)
    json_objc["username"] = DICT.get("screen_name", raw_tweet)
    json_objc["body"] = DICT.get("full_text", raw_tweet, default="Tweet-Body-Empty")
    urls = DICT.get("urls", raw_tweet)
    url = False
    if urls:
        for item in urls:
            url = DICT.get("expanded_url", item, default=False)
            if url:
                break
    if not url:
        url = DICT.get("url", raw_tweet)
    json_objc["url"] = url
    json_objc["published_date"] = DATE.parse(DICT.get("created_at", raw_tweet))
    json_objc["date_created"] = DATE.parse_date(DATE.get_now_date())
    json_objc["client"] = "twitter client"
    json_objc["source"] = "twitter"
    json_objc["source_url"] = "www.twitter.com"
    # + Twitter Core
    json_objc["retweet_count"] = DICT.get("retweet_count", raw_tweet)
    json_objc["verified"] = DICT.get("verified", raw_tweet)
    return json_objc
