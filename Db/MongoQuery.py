from bson.objectid import ObjectId
from pymongo import cursor
from FWEB import LIST, DICT, DATE, MongoCore, Log
Log = Log("MongoQuery")


class Find:
    collection_name = ""
    collection = None

    def __init__(self, collection_name, collection):
        self.collection_name = collection_name
        self.collection = collection

    def find_metaverse_for_date_and_score(self, date: str):
        # records = self.collection.find({ "date": "January 24 2022", "raw_hookups.category_scores.metaverse": { "$gte": 50 } })
        # _query = {"date": f"{date}", "raw_hookups.category_scores.metaverse.0": {"$gte": f"{score}"}}
        # _query = {"date": f"{date}", "raw_hookups.category_scores.metaverse.0": {"$gt": score}}
        _query = {"date": f"{date}", "raw_hookups.category": "metaverse"}
        records = self.collection.find(_query)
        return records

    def find_list_of_record_ids_where_date(self, date: str) -> cursor:
        """ -> RETURN List of all Record ID's for Date. <- """
        if not date:
            date = MongoCore.to_db_date(DATE.get_now_date())
        # raw_records = self.collection.distinct("_id", {"date": date})
        raw_records = self.collection.find({"date": date})
        return raw_records

    def find_record_where_id(self, _id: str) -> list:
        """ -> RETURN Single Record for ID in List. <- """
        record = self.collection.find({"_id": ObjectId(str(_id))})
        record_list = list(record)
        Log.d(f"{record_list}")
        return LIST.get(0, record_list)

    def find_record_where_index_date(self, date: str, _index=-999) -> dict:
        """ -> RETURN Single Record at Index for Date. <- """
        temp = self.find_records_where_date(date)
        result = list(temp)
        count = len(result)
        if _index == -999:
            userInput = input(f"{count} records available. Return which record?")
            if userInput.isdigit() and int(userInput) > count or int(userInput) < -1:
                indexRecord = LIST.get(int(userInput) - 1, result)
            else:
                indexRecord = LIST.get(_index, result)
        else:
            indexRecord = LIST.get(_index, result)
        return_obj = DICT.get("_id", indexRecord)
        Log.d(f"{return_obj}")
        return return_obj

    def find_records_where_date(self, date: str, toDict=False) -> cursor or dict:
        """ -> RETURN Cursor of all Records for Date. <- """
        result = self.collection.find({"date": date})
        if toDict:
            return MongoResearch.to_counted_dict(result)
        else:
            return result

    def find_records_where_count(self, date: str, limit=1000, toDict=False) -> list or dict:
        """ -> RETURN List/Dict of all Records for Date with count under limit. <- """
        result = self.collection.find({"date": date, "count": { "$lte": limit } })
        if toDict:
            _result = MongoResearch.to_counted_dict(result)
        else:
            _result = list(result)
        return _result

    def find_ids_for_last_num_days(self, days=7) -> list:
        """ -> RETURN Dict of all Records for Date. <- """
        dates = DATE.get_last_x_days(days=days)
        temp_list = []
        for date in dates:
            temp = self.find_list_of_record_ids_where_date(date)
            temp_list.append(temp)
        results = LIST.flatten(temp_list)
        return results
