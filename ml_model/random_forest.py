import numpy as np
import requests
import random
from operator import itemgetter
from database import mongo_methods
import pandas as pd


# dataset = pd.read_csv('D:\Datasets\petrol_consumption.csv')
# dataset.head()
# pd.DataFrame(d.items(), columns=['Date', 'DateValue'])  # convert json to columns dataframe
def extract_values_from_json(dict_from_mongo):
    # list_values_test = ['name', 'address']
    list_values = ['link', 'p', 'div', 'script', 'img', 'input', 'form', 'href', 'src', 'h1', 'h2']
    list_to_train = []
    # result = list(map(itemgetter(str(i)), train))
    for i in list_values:
        # print([list_values[i] for key, value in train.items() for d in value])
        # list_to_train.append(map(itemgetter(str(i)), train))
        # list_to_train.append(list(sub [str(i)] for sub in dict_from_mongo))
        list_to_train.append(list(sub[i] for sub in dict_from_mongo))

    print(list_to_train)
    import itertools

    ab = itertools.chain(*list_to_train)
    print(list(ab))

    return ab


def read_from_json(dataset):
    # Reading JSON
    pd.read_json(dataset)
    print(pd.read_json(dataset))


def read_from_api():
    """
    Read from Api
    :return: response of object
    """
    return requests.get('http://www.starcapital.de/test/Res_Stockmarketvaluation_FundamentalKZ_Tbl.php')


def run_model_random_forest(X, y):
    X = X.shape
    y = y.shape
    print('----------')
    print(X)
    print('----------')
    print(y)


    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, recall_score, confusion_matrix

    X_train, X_test, y_train, y_test = train_test_split(
        list(X), list(y), train_size=0.7, random_state=3
    )
    rfc = RandomForestClassifier()
    rfc.fit(X_train, y_train)
    y_pred = rfc.predict(X_test)

    print(accuracy_score(y_test, y_pred))
    print(recall_score(y_test, y_pred))
    print(confusion_matrix(y_test, y_pred))


def split_train_test():
    mg = mongo_methods.MongoAcess()
    doc_list = mg.read_to_ml(3)
    # print(doc_list)
    random.shuffle(doc_list)
    cut_point = int(len(doc_list) * 0.7)
    train_ds = doc_list[:cut_point]
    test_ds = doc_list[cut_point:]
    print('train ' + str(train_ds))
    print('test ' + str(test_ds))
    return train_ds, test_ds


def model_dataset(dataset):
    df = pd.DataFrame(dataset)

    del df['_id']
    print(df)
    return df


if __name__ == '__main__':
    train, test = split_train_test()
    prep_train = model_dataset(train)
    prep_test = model_dataset(test)
    run_model_random_forest(prep_train, prep_test)
    # [d['value'],d['address']  for d in l]
    # result = [d['name'] for d in train if 'name' in d]
    # print(result)

    values_list = extract_values_from_json(train)
    print('---------')
    print(values_list)
