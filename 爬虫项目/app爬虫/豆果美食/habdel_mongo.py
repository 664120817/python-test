import pymongo
from pymongo.collation import Collation

class Connet_mongo(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host='localhost', port=27017)
        self.db_data =self.client['dou_guo_meishi']['dou_guo_meishi_item']
    def insert_item(self,item):

        self.db_data.insert_one(dict(item))

mongo_info = Connet_mongo()
