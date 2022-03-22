from FWEB import DICT, Log
Log = Log("MongoAddUpdate")

MAX_THRESHOLD = 500

class MongoAddUpdate:
    name = ""
    collection = None

    def __init__(self, collection_name, collection):
        super().__init__()
        self.name = collection_name
        self.collection = collection

    """-> UPDATE MODE <-"""
    def update_raw_hookups(self, _id, _query, _count):
        """ PUBLIC METHOD """
        if _count <= MAX_THRESHOLD:
            self.update_record(_id, _query)
            return True
        # -> Queue Loop
        # -> Prep
        temp_list = []
        temp_count = 0
        full_count = 0
        _raw_hookups = DICT.get("raw_hookups", _query)
        for hookup in _raw_hookups:
            if temp_count >= MAX_THRESHOLD:
                _query["raw_hookups"] = temp_list
                _query["count"] = temp_count
                self.update_record(_id, _query)
                temp_list = []
                temp_count = 0
                continue
            # -> temp_list isn't over "1500" yet.
            temp_list.append(hookup)
            temp_count += 1
            full_count += 1
        # -> If any hookups are left over, insert them. (Might not be 500 left)
        if len(temp_list) > 0:
            _query["raw_hookups"] = temp_list
            _query["count"] = temp_count
            self.update_record(_id, _query)

    """-> NEW MODE <-"""
    def insert_raw_hookups(self, _query):
        """ PUBLIC METHOD """
        if _query["count"] > MAX_THRESHOLD:
            # -> Prep
            temp_list = []
            temp_count = 0
            full_count = 0
            for hookup in _query["raw_hookups"]:
                if temp_count >= MAX_THRESHOLD:
                    _query["raw_hookups"] = temp_list
                    _query["count"] = temp_count
                    self.insert_record(query=_query)
                    temp_list = []
                    temp_count = 0
                    continue
                # -> temp_list isn't over "1500" yet.
                temp_list.append(hookup)
                temp_count += 1
                full_count += 1
            # -> If any hookups are left over, insert them. (Might not be 500 left)
            if len(temp_list) > 0:
                _query["raw_hookups"] = temp_list
                _query["count"] = temp_count
                self.insert_record(query=_query)
        else:
            self.insert_record(query=_query)

    def insert_record(self, query: {}):
        """ PRIVATE METHOD """
        try:
            _query = DICT.removeKeyValue("_id", query)
            self.collection.insert_one(_query)
            Log.s(f"NEW Record created in DB=[ {self.name} ], Date=[ {_query['date']} ]")
        except Exception as e:
            Log.e(f"Failed to save record in DB=[ {self.name} ], Date=[ {query['date']} ]", error=e)

    def update_record(self, _id, setQuery: {}):
        """ PRIVATE METHOD """
        try:
            newQuery = {"$set": setQuery }
            self.collection.update_one({"_id": _id}, newQuery, upsert=True)
            Log.s(f"UPDATED {str(_id)} Successfully in DB=[ {self.name} ]")
        except Exception as e:
            Log.e(f"UPDATED {_id} FAILED. DB=[ {self.name} ], Date=[ {setQuery['date']} ]", error=e)