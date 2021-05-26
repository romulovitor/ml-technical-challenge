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
        self.host = 'localhost'
        self.port = '27017'
        self.string_conection = 'mongodb://' + self.db_user + ':' + self.db_pass + '@' + self.host + ':' + self.port

    def insert_mongo(self, characteristic):
        client = MongoClient(self.string_conection)
        mydb = client['scraping_link']
        mycol = mydb["links"]
        try:
            dct_x = mycol.insert_one(characteristic)
            print(dct_x)
            return dct_x
        except:
            print("It was not possible save in database")

    def read_link(self, link):
        client = MongoClient(self.string_conection)
        mydb = client['scraping_link']
        mycol = mydb["links"]
        myquery = {"link": "" + str(link) + ""}
        print(myquery)
        mydoc = mycol.find(myquery)
        print(mydoc)
        docs_list = []
        for x in mydoc:
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
            x = x+1
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

    def convert_to_csv(self):
        # pd.DataFrame(d.items(), columns=['Date', 'DateValue'])
        pass


if __name__ == '__main__':
    mongo = MongoAcess()
    # mongo.insert_mongo()
    # mongo.read_all()
    mongo.read_to_ml_teste(5)
    # mongo.read_link("https://en.wikipedia.org/wiki/Algorithm") OK
