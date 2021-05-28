import requests
from bs4 import BeautifulSoup
from datetime import datetime
from database import mongo_methods
import argparse


def get_request(url_request):
    return requests.get(url_request)


def parse_request(page_returned, depth):
    """
        :param depth:
        :param page_returned: It have the main link requested
        :return: List of links found
        """
    soup = BeautifulSoup(page_returned.text, "html.parser")
    print("The href links are :")
    list_appearances = []
    total_appearances = 0
    for link in soup.select('a[href^="http"]'):
        if depth > 0:
            print(link.get('href'))
            list_appearances.append(link.get('href'))
        total_appearances = total_appearances + 1
        depth = depth - 1
    return list_appearances, total_appearances


def parse_request_wrap(url, page_returned, depth):
    """
    :param page_returned: It have the main link requested
    :return: List of links found
    """
    infor_depth = depth
    mongo = mongo_methods.MongoAcess()
    list_appearances, total_appearances = parse_request(page_returned, depth)
    i = 0
    while 0 < depth:
        if i == 0:
            print('----------- FIRST --------------------')
            print("URL " + str(url), "PAGE " + str(page_returned), "TOTAL " + str(total_appearances))
            print(extract_characteristic(url, page_returned, len(list_appearances)))
            dict_entity = extract_characteristic(url, page_returned, total_appearances)
            mongo.insert_mongo(dict_entity)
        else:
            content_page_others = get_request(list_appearances[i])

            print(list_appearances[i])
            url_list = list_appearances[i]
            list_appearances_other, total_appearances_others = parse_request(content_page_others, infor_depth)
            print('----------- OTHERS --------------------')
            print(url_list, content_page_others, total_appearances_others)
            dict_entity = extract_characteristic(url_list, content_page_others, total_appearances_others)
            mongo.insert_mongo(dict_entity)
            print("------- after insert ", url_list, content_page_others, len(list_appearances_other))
        i = i + 1
        depth = depth - 1
    return


def set_datetime():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string


def array_characteristic(dict_page):
    array_list = []
    for tag_values in dict_page:
        array_list.append(tag_values.values())
    return array_list


def extract_characteristic(url_returned, html, total_appearences):
    dict_full_characteristic = {}
    soup = BeautifulSoup(html.text, "html.parser")
    list_characteristic = ['p', 'div', 'script', 'img', 'input', 'form', 'href', 'src', 'h1', 'h2']
    dict_full_characteristic['link'] = url_returned
    dict_full_characteristic['total_appearences'] = total_appearences
    dict_full_characteristic['timestamp'] = set_datetime()
    for i in list_characteristic:
        dict_full_characteristic[f'{i}'] = len(soup.find_all(f'{i}'))

    return dict_full_characteristic


# implementing search and save in database
# built docker composer to API and mongodb
# implemente read and list on mongodb
# make reprocesse crawler
def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--url", help="Link to make scraping.",
                        default='https://en.wikipedia.org/wiki/Algorithm')
    parser.add_argument("-d", "--depth", help="How many link the fucntion will get in after the first.", default=15)
    return parser.parse_args()


if __name__ == '__main__':
    args = read_args()
    #url = "https://stackoverflow.com/questions/13745648/running-bash-script-from-within-python/13745968"
    print("Echo:", args.url)
    content_page = get_request(args.url)
    parse_request_wrap(args.url, content_page, args.depth)
