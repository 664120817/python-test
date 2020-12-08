import pymongo
from pymongo.collation import Collation

class Connet_mongo(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host='localhost', port=27017)
        self.db_data =self.client['douyin_fs']['douyin_fs_info']
    def insert_item(self,item):

        self.db_data.insert_one(dict(item))

mongo_info = Connet_mongo()

class Connet_mongo1(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host='localhost', port=27017)
        self.db_data =self.client['douyin_gr']['douyin_gr_info']
    def insert_item(self,item):

        self.db_data.insert_one(dict(item))

mongo_info1 = Connet_mongo1()