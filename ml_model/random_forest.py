from database import mongo_methods
import pandas as pd
import numpy as np

from scraping import get_request, parse_request_wrap


def get_prediction(link):
    mg = mongo_methods.MongoAcess()
    result_from_db = mg.read_from_db_return_list(link)
    if len(result_from_db) == 0:  # new link
        print("Novo link")
        content_page = get_request(link)
        parse_request_wrap(link, content_page, 1)
        result_from_db = mg.read_from_db_return_list(link)
        x_train, x_label = prepared_model(result_from_db)
        predict = build_model(x_train)
        result = predict[0]
        mg.update_collection_link(link, predict)
        return result

    elif any("prediction" in s for s in result_from_db):
        print("Possui a predição já armazenada")
        prediction_from_db = mg.read_by_link(link)
        return prediction_from_db
    else:
        print("Existe mas não foi calculado a predição")
        print(result_from_db)
        x_train, x_label = prepared_model(result_from_db)
        predict = build_model(x_train)
        result = predict[0]
        mg.update_collection_link(link, result)
        return result


def run_model(regressor_returned, base_predict):  # , dict_link
    return regressor_returned.predict(base_predict)


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
    return regressor


def split_train_test():
    """
    Read and split by 70-30 the datas from dataset in test and training
    default number subject = 15
    :return: list train and test
    """
    mg = mongo_methods.MongoAcess()
    doc_list = mg.read_to_ml(15)
    cut_point = int(len(doc_list) * 0.7)
    train_ds = doc_list[:cut_point]
    test_ds = doc_list[cut_point:]
    # print('train ' + str(train_ds))
    # print('test ' + str(test_ds))
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


