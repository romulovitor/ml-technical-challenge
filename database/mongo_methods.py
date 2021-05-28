import json

import pymongo
from bson import json_util
from pymongo import MongoClient
import math


def rand_function():
    return math.floor(math.r * 3)


class MongoAcess():

    def __init__(self):
        self.db_user = 'romulo'
        self.db_pass = 'toor'
        self.host = 'mongo'
        self.port = '27017'
        self.string_conection = 'mongodb://' + self.db_user + ':' + self.db_pass + '@' + self.host + ':' + self.port

    def insert_mongo(self, characteristic):
        client = MongoClient(self.string_conection)
        mydb = client['scraping_link']
        mycol = mydb["links"]
        try:
            dct_x = mycol.insert_one(characteristic)
            print("Save in database")
            return dct_x
        except:
            print("It was not possible save in database")

    def update_collection_link(self, link, prediction):
        client = MongoClient(self.string_conection)
        mydb = client['scraping_link']
        mycol = mydb["links"]
        myquery = {"link": str(link)}
        newvalues = {"$set": {"prediction": prediction}}

        mycol.update_one(myquery, newvalues)
        # print "customers" after the update:
        for x in mycol.find():
            print(x)
        return x

    def read_by_link_from_api(self, link):
        client = MongoClient(self.string_conection)
        mydb = client['scraping_link']
        mycol = mydb["links"]
        myquery = {"link": "" + str(link) + ""}
        print(myquery)
        mydoc = mycol.find(myquery)
        print(mydoc)
        docs_list = []
        result = list(mydoc)
        if len(result)!=0:
            for x in mydoc:
                if x is None:
                    docs_list.append(x)
                print(x)
        return json.dumps(docs_list, default=json_util.default)


    def read_by_link(self, link):
        client = MongoClient(self.string_conection)
        mydb = client['scraping_link']
        mycol = mydb["links"]
        myquery = {"link": "" + str(link) + ""}
        print(myquery)
        mydoc = mycol.find(myquery)
        print(mydoc)
        docs_list = []
        result = list(mydoc)
        if len(result)!=0:
            for x in mydoc:
                if x is None:
                    docs_list.append(x)
                print(x)
        return json.dumps(docs_list, default=json_util.default)


    def read(self):
        client = MongoClient(self.string_conection)
        mydb = client['scraping_link']
        mycol = mydb["customers"]
        myquery = {"link": "https://en.wikipedia.org/wiki/Algorithm"}
        mydoc = mycol.find(myquery)
        docs_list = []
        for x in mydoc:
            docs_list.append(x)
            print(x)
        return json.dumps(docs_list, default=json_util.default)

    def read_from_db_return_list(self, link):
        import random
        client = MongoClient(self.string_conection)
        mydb = client['scraping_link']
        mycol = mydb["links"]
        myquery = {"link": str(link)}
        mydoc = mycol.find(myquery)
        #mydb.mycol.find({'predicition': {'$exists': True}})
        docs_list = []
        for x in mydoc:
            docs_list.append(x)
            print(x)
        return docs_list

    def read_to_ml(self, len_sample):
        import random
        client = MongoClient(self.string_conection)
        mydb = client['scraping_link']
        mycol = mydb["links"]
        docs_list = []
        x = 0
        while x < len_sample:
            count = mycol.estimated_document_count()
            print(mycol.find()[random.randrange(count)])
            docs_list.append(mycol.find()[random.randrange(count)])
            x = x + 1
        return docs_list

    def read_all(self):
        client = MongoClient(self.string_conection)
        mydb = client['scraping_link']
        mycol = mydb["links"]
        docs_list = []
        for x in mycol.find():
            docs_list.append(x)
            print(x)
        return json.dumps(docs_list, default=json_util.default)


if __name__ == '__main__':
    mongo = MongoAcess()
    # mongo.insert_mongo()
    # mongo.read_all()
    mongo.read_to_ml_teste(5)
    # mongo.read_link("https://en.wikipedia.org/wiki/Algorithm") OK
