from pymongo import cursor
# from Engine.Parser.HookupParser import Parser
from FWEB.Futils import LIST, DICT, Ext
from FWEB.rsLogger import Log
from FWEB.Db.MongoCore import MongoCore
from FWEB.Db.MongoQuery import Find
from FWEB.Db.MongoAddUpdate import MongoAddUpdate

Log = Log("MongoArchive")

class MongoArchive(MongoCore):
    _save = None
    _find = None
    query_insert = {"date": "", "raw_hookups": [], "count": 0}
    query_update = {"$set": {"raw_hookups": [], "count": 0}}

    def __init__(self):
        super().__init__()
        self._find = Find(collection_name="archive", collection=self.c_archive)
        self._save = MongoAddUpdate(collection_name="archive", collection=self.c_archive)

    def get_list_of_record_ids_where_date(self, date=None, toList=False):
        if not toList:
            return self._find.find_list_of_record_ids_where_date(date=date)
        else:
            temp = self._find.find_list_of_record_ids_where_date(date=date)
            return MongoCore.to_list(temp)

    def get_record_where_id(self, _id: str) -> list:
        """ -> RETURN Single Record for ID in List. <- """
        return self._find.find_record_where_id(_id=_id)

    def get_record_where_index_date(self, date: str, _index=-999) -> dict:
        """ -> RETURN Single Record at Index for Date. <- """
        return self._find.find_record_where_index_date(date, _index)

    def get_records_where_date(self, date: str, toDict=False) -> cursor or dict:
        """ -> RETURN Cursor of all Records for Date. <- """
        return self._find.find_records_where_date(date, toDict)

    def get_records_where_count(self, date: str, limit=1000, toDict=False) -> list or dict:
        """ -> RETURN List/Dict of all Records for Date with count under limit. <- """
        return self._find.find_records_where_count(date=date, limit=limit, toDict=toDict)

    def get_ids_for_last_num_days(self, days=7) -> list:
        """ -> RETURN Dict of all Records for Date. <- """
        return self._find.find_ids_for_last_num_days(days=days)

    def get_hookups_from_archive(self, date):
        results = []
        records = self.get_list_of_record_ids_where_date(date, toList=True)
        for record in records:
            _id = DICT.get("_id", record)
            _record = self.get_record_where_id(_id)
            _key_date = DICT.get("date", _record)
            _raw_hookups = DICT.get("raw_hookups", _record)
            if _raw_hookups:
                parsed_hookups = Parser.parse_list(_raw_hookups, parseAll=True)
                temp = (_id, _key_date, parsed_hookups)
                results.append(temp)
        return results


    """ 
        INIT ADDING NEW ARCHIVES
    -> 01/22: Cleaned and Updated
    """
    @Ext.safe_args
    def addUpdate_archives(self, list_of_hookups):
        from Mongodb.MongoQuery import Find
        _find = Find("archive", self.c_archive)
        """ GLOBAL METHOD """
        # -> Create Dict of Dates that hold archives for that date.
        hookups_by_date = Hookup.sort_by_date(list_of_hookups)
        # -> Master Loop Dict of Dates that hold archives for that date.
        for key_date in hookups_by_date.keys():
            # -> 1. NEW -> Organize New Archives
            new_hookups = hookups_by_date[key_date]
            new_archive_ready = Hookup.convert_list_to_archive_json(new_hookups)
            # -> 2. OLD -> Get current Archives
            db_hookups = self._find.find_records_where_count(key_date, toDict=True)
            lowest = self.get_lowest_count(db_hookups)
            if lowest:
                lowest_record = LIST.get(2, lowest)
                _id = LIST.get(0, lowest)
                db_archive_ready = Hookup.convert_list_to_archive_json(DICT.get("raw_hookups", lowest_record))
            else:
                _id = False
                db_archive_ready = False
            # -> 3. ALL -> Prepare Parameters for Insert/Update.
            full_archive_ready = self.remove_duplicates((LIST.merge_hookups(new_archive_ready, db_archive_ready)))
            new_archive_count = len(new_archive_ready)  # YES save NEW
            full_archive_count = len(full_archive_ready)  # YES save UPDATE
            # -> 4. SAVE -> Initiate Insert/Update Process for Archives.
            if db_archive_ready and len(db_archive_ready) < 500 and full_archive_count < 500:
                # -> UPDATE MODE
                query_update = {"date": key_date, "raw_hookups": full_archive_ready, "count": full_archive_count}
                self._save.update_raw_hookups(_id, query_update, full_archive_count)
            else:
                # -> NEW MODE
                self.query_insert["raw_hookups"] = new_archive_ready
                self.query_insert["count"] = new_archive_count
                self.query_insert["date"] = key_date
                self._save.insert_raw_hookups(self.query_insert)

    """ -> HELPER FUNCTIONS <- """
    @staticmethod
    def remove_duplicates(hookups):
        return DICT.remove_duplicates("body", hookups)

    @staticmethod
    def are_identical(hookup1, hookup2, outOf=2) -> bool:
        count = 0
        tempBody1 = DICT.get("body", hookup1)
        tempTitle1 = DICT.get("title", hookup1)
        tempUrl1 = DICT.get("url", hookup1)
        tempBody2 = DICT.get("body", hookup2)
        tempTitle2 = DICT.get("title", hookup2)
        tempUrl2 = DICT.get("url", hookup2)
        if tempTitle1 == tempTitle2:
            count += 1
        if tempBody1 == tempBody2:
            count += 1
        if tempUrl1 == tempUrl2:
            count += 1
        if count > outOf:
            return True
        else:
            return False

    @staticmethod
    def get_lowest_count(temp_dict):
        if not temp_dict:
            return False
        lowest_count = 1000
        lowest_record = {}
        lowest_id = None
        for record in temp_dict.keys():
            count = DICT.get("count", temp_dict[record])
            if count < lowest_count:
                lowest_count = count
                lowest_record = temp_dict[record]
                lowest_id = record
        return lowest_id, lowest_count, lowest_record


# if __name__ == '__main__':
#     temp_date = "January 25 2022"
#     db = MongoArchive()
    # ids = db.get_list_of_record_ids_where_date(temp_date)
    # for id in ids:
    #     print(id)
    # record = db.get_record_where_id("61f2e03e86bd34d1e4c694b7")
    # count = DICT.get("count", record)
    # print(count)
    # print(db.get_records_where_date(temp_date))
    # print(db.get_record_where_index_date(temp_date))
    # test = db.get_records_where_date(temp_date, toDict=True)
    # print(test)
    # count = 0
    # for i in t:
    #     print(i)
    #     count += 1
    # print("Records:", count)


