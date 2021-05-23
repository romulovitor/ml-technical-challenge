import json

import pymongo
from bson import json_util
from pymongo import MongoClient


# def insert_mongo():
#     client = MongoClient('mongodb://romulo:toor@localhost:27017')
#     mydb = client['scraping_link']
#     mycol = mydb["customers"]
#     mydict = {"name": "John4", "address": "Highway 37"}
#     x = mycol.insert_one(mydict)
#     print(x)
#
#
# def read():
#     client = MongoClient('mongodb://romulo:toor@localhost:27017')
#     mydb = client['scraping_link']
#     mycol = mydb["customers"]
#     myquery = {"name": "John4"}
#     mydoc = mycol.find(myquery)
#     for x in mydoc:
#         print(x)


class MongoAcess():

    def __init__(self):
        self.db_user = 'romulo'
        self.db_pass = 'toor'
        self.host = 'mongo'
        self.port = '27017'
        self.string_conection = 'mongodb://' + self.db_user + ':' + self.db_pass + '@' + self.host + ':' + self.port

    def insert_mongo(self):
        client = MongoClient(self.string_conection)
        mydb = client['scraping_link']
        mycol = mydb["customers"]
        mydict = {"name": "John4", "address": "Highway 37"}
        dct_x = {}
        dct_x = mycol.insert_one(mydict)
        print(dct_x)
        return dct_x

    def read(self):
        client = MongoClient(self.string_conection)
        mydb = client['scraping_link']
        mycol = mydb["customers"]
        myquery = {"name": "John4"}
        mydoc = mycol.find(myquery)
        docs_list = []
        for x in mydoc:
            docs_list.append(x)
            print(x)
        return json.dumps(docs_list, default=json_util.default)

    def read1(self):
        client = MongoClient(self.string_conection)
        mydb = client['scraping_link']
        mycol = mydb["customers"]
        myquery = {"name": "John4"}
        mydoc = mycol.find(myquery)
        docs_list=[]
        for x in mydoc:
            docs_list.append(x)
            print(x)
        return json.dumps(docs_list, default=json_util.default)
    def convert_to_csv(self):
        # pd.DataFrame(d.items(), columns=['Date', 'DateValue'])
        pass


if __name__ == '__main__':
    mongo = MongoAcess()
    # mongo.insert_mongo()
    mongo.read()
