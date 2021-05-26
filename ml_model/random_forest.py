#import pandas as pd
import numpy as np
import requests
import random

from database import mongo_methods

#dataset = pd.read_csv('D:\Datasets\petrol_consumption.csv')
#dataset.head()
#pd.DataFrame(d.items(), columns=['Date', 'DateValue'])  # convert json to columns dataframe


def read_from_api():
    """
    Read from Api
    :return: response of object
    """
    return requests.get('http://www.starcapital.de/test/Res_Stockmarketvaluation_FundamentalKZ_Tbl.php')


def parse_request(request):
    j = request.json()
    # df = pd.DataFrame([[d['v'] for d in x['c']] for x in j['rows']],
    #                   columns=[d['label'] for d in j['cols']])
    # df.head()


def split_train_test():
    mg = mongo_methods.MongoAcess()
    thing_list = list(mg.read_to_ml())
    random.shuffle(thing_list)
    cut_point = int(len(thing_list) * 0.7)
    train_ds = thing_list[:cut_point]
    test_ds = thing_list[cut_point:]
    print('train '+str(train_ds))
    print('test '+str(test_ds))
    return train_ds, test_ds


if __name__ == '__main__':
    train, test = split_train_test()