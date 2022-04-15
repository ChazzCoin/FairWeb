potential_keys = {
        "author": ["author", "authors", "screen_name", "user", "name"],
        "title": ["title"],
        "body": ["body", "text", "full_text", "selftext"],
        "description": ["description", "meta_description"],
        "published_date": ["published_date", "publish_date", "created_at", "parsely-pub-date"],
        "url": ["url", "urls"],
        "imgUrl": ["imgUrl", "meta_img", "profile_image_url"],
        "tags": ["tags", "parsely-tags", "keywords", "meta_keywords", "news_keywords", "parsely-section", "parsely-type"],
        "source_url": ["source_url", "source"],
        "tickers": ["tickers"],
        "companies": ["companies"],
        "up_votes": ["ups"],
        "comments": ["comments", "comment"]
    }

def keys(key) -> []:
    return potential_keys[key]