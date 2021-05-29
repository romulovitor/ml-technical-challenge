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
        """
        Insert in the database based in the parameters came from extract_characteristic
        :param characteristic: a dictionary with all datas
        :return: print the sucess or failure of process
        """
        client = MongoClient(self.string_conection)
        mydb = client['scraping_link']
        mycol = mydb["links"]
        try:
            mycol.insert_one(characteristic)
            print("Save in database")
        except:
            print("It was not possible save in database")

    def update_collection_link(self, link, prediction):
        """
        To save the new field "prediction"
        :param link: url
        :param prediction: value calculated by model
        :return: None
        """
        client = MongoClient(self.string_conection)
        mydb = client['scraping_link']
        mycol = mydb["links"]
        try:
            mycol.update({"link": str(link)}, {'$set': {"prediction": prediction}})
            print("It was save with sucess")
        except:
            print("Occurred an error during the update")

    def read_by_link(self, link):
        """
        Retur the prediction from a url already calculated
        :param link: url
        :return: the prediction storage
        """
        client = MongoClient(self.string_conection)
        mydb = client['scraping_link']
        mycol = mydb["links"]
        myquery = {"link": "" + str(link) + ""}
        print(myquery)
        try:
            mydoc = mycol.find(myquery)
            print(mydoc)
            for x in mydoc:
                return x['prediction']
        except:
            print("Error to find the prediction")

    def read_from_db_return_list(self, link):
        client = MongoClient(self.string_conection)
        mydb = client['scraping_link']
        mycol = mydb["links"]
        myquery = {"link": str(link)}
        try:
            mydoc = mycol.find(myquery)
            docs_list = []
            for x in mydoc:
                docs_list.append(x)
            return docs_list
        except:
            print("Error to recover the list from the link")

    def read_to_ml(self, len_sample):
        """
        Get the random documents to generate the dataset to model
        :param len_sample: How many documents
        :return: list of documents
        """
        import random
        client = MongoClient(self.string_conection)
        mydb = client['scraping_link']
        mycol = mydb["links"]
        docs_list = []
        x = 0
        try:
            while x < len_sample:
                count = mycol.estimated_document_count()
                print(mycol.find()[random.randrange(count)])
                docs_list.append(mycol.find()[random.randrange(count)])
                x = x + 1
            return docs_list
        except:
            print("Error to get data to generate the model")
