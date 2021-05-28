import numpy as np
import requests
import random
from operator import itemgetter
from database import mongo_methods
import pandas as pd
import numpy as np

from scraping import array_characteristic, get_request, parse_request_wrap


def read_from_json(dataset):
    # Reading JSON
    pd.read_json(dataset)
    print(pd.read_json(dataset))


def get_prediction(link):
    mg = mongo_methods.MongoAcess()
    result_from_db = mg.read_from_db_return_list(link)
    if len(result_from_db) == 0:
        content_page = get_request(link)
        #parse_request_wrap(link, content_page, 1)

        # result_from_db = mg.read_from_db_return_list(link)
        # x_train, x_label = prepared_model(result_from_db)
        # print(x_train)
        # ml = ModelRandomForest
        # predict = ml.__init__(to_predict=x_train)
        # result_from_db = mg.update_collection_link(link, predict)


    else:
        x_train, x_label = prepared_model(result_from_db)
        print('--- ELSE -------')
        # List of dict
        #print(result_from_db)
        #print(x_train)
        predict = build_model(x_train)
        return predict
        #print(predict)
        #result_from_db = mg.update_collection_link(link, predict)

        # trained_model = train_model_random_forest(x_train, x_label)

        # run_model(trained_model, x_train)
        # print(run_model(trained_model, x_train))




def run_model(regressor_returned, base_predict):  # , dict_link

    return regressor_returned.predict(base_predict)

    # mongo = mongo_methods.MongoAcess()
    #
    # if mongo.read_link(dict_link):
    #     return dict_link['prediction']
    #     # return the json in API
    # else:
    #     dict_link['prediction'] = regressor_returned.fit()
    #     mongo.update_collection_link(dict_link['link'])

    # mongo.insert_mongo(dict_link)

    # if read_link(link):
    # update the link
    # else:
    #    insert_mongo(dict_characteristic)


def prepared_model_deprecated(x, y):
    """
        Receive a list of dictionary from mongoDB
        :param x: List from mongo
        :return: Dataframe prepared to use in the model
        """
    x_train = model_dataset(x)
    x_train_label = x_train['total_appearences']
    del x_train['total_appearences']

    # y_test = model_dataset(y)
    # y_test_label = y_test['total_appearences']
    # del y_test['total_appearences']

    x_train = np.reshape(x_train, (int(len(x_train)), 10))
    # y_test = np.reshape(y_test, (int(len(y_test)), 10))

    return x_train, x_train_label


def prepared_model(x):
    """
    Receive a list of dictionary from mongoDB
    :param x: List from mongo
    :return: Dataframe prepared to use in the model
    """
    x_train = model_dataset(x)
    x_train_label = x_train['total_appearences']
    del x_train['total_appearences']
    x_train = np.reshape(x_train, (int(len(x_train)), 10))
    return x_train, x_train_label


def train_model_random_forest(x_train, x_train_label):
    """
    Apply the train base in the model and let the model prepared to receive the user input to predict
    :param x_train: dataset clean to apply the model
    :param x_train_label: Ours target the true values
    :return: regressor, contain our model
    """
    from sklearn.ensemble import RandomForestRegressor
    regressor = RandomForestRegressor(n_estimators=100, max_depth=10)
    regressor.fit(x_train, x_train_label)
    # a = [3,12,9,8,5,7,6,2,45,3]
    # y = np.reshape(a, (int(len(a)), 10))
    # regressor.predict(y)

    return regressor
    # regressor = RandomForestRegressor(n_estimators=100, depth=10)
    # regressor.fit(X, X_label)

    # score = regressor.score(y, y_label)
    # y_predict = regressor.predict(y)

    # print(y_predict)
    # print(y_label)
    # print(score)


def split_train_test():
    """
    Read and split by 70-30 the datas from dataset in test and training
    default number subject = 15
    :return: list train and test
    """
    mg = mongo_methods.MongoAcess()
    doc_list = mg.read_to_ml(15)
    # print(doc_list)
    # random.shuffle(doc_list)
    cut_point = int(len(doc_list) * 0.7)
    train_ds = doc_list[:cut_point]
    test_ds = doc_list[cut_point:]
    print('train ' + str(train_ds))
    print('test ' + str(test_ds))
    return train_ds, test_ds


def model_dataset(dataset):
    """
    Receive a dict and parse to dataframe. Remove the not used columns.
    :param dataset:
    :return:
    """
    df = pd.DataFrame(dataset)
    del df['_id']
    del df['timestamp']
    del df['link']
    # print(df)
    return df


def build_model(to_predict):
    """
    train the model based in a default number of subjects
    Receive the number to predict baseade in the model
    :return: prediciton
    """
    train, test = split_train_test()
    x_train, x_label = prepared_model(train)
    trained_model = train_model_random_forest(x_train, x_label)
    prediction_result = run_model(trained_model, to_predict)
    return prediction_result



if __name__ == '__main__':
    train, test = split_train_test()
    x_train, x_label = prepared_model(train)
    print(x_train)
    trained_model = train_model_random_forest(x_train, x_label)
    # trained_model=train_model_random_forest(x_train, x_label)

    #run_model(trained_model)

    # [d['value'],d['address']  for d in l]
    # result = [d['name'] for d in train if 'name' in d]
    # print(result)

    # values_list = extract_values_from_json(train)
    # print('---------')
    # print(values_list)
