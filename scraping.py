import requests
from bs4 import BeautifulSoup
from datetime import datetime
from database import mongo_methods
import argparse


def get_request(url_request):
    return requests.get(url_request)


def parse_request(page_returned, depth):
    """  Responsible to get the links from the pages using a specific library
        :param depth: How many request will make
        :param page_returned: It have the main link requested
        :return: List of links found and total of appearances
        """
    soup = BeautifulSoup(page_returned.text, "html.parser")
    list_appearances = []
    total_appearances = 0
    for link in soup.select('a[href^="http"]'):
        if depth > 0:
            print(link.get('href'))
            list_appearances.append(link.get('href'))
        total_appearances = total_appearances + 1
        depth = depth - 1
    return list_appearances, total_appearances


def parse_request_wrap(url, page_returned, depth, src):
    """
    :param url: link collected
    :param depth: how many time will make the scraping
    :param src: flag to know if request from localhost ou docker
    :param page_returned: It have the main link requested
    :return: List of links found
    """
    infor_depth = depth
    mongo = mongo_methods.MongoAcess()
    list_appearances, total_appearances = parse_request(page_returned, depth)
    i = 0
    while 0 < depth:
        if i == 0:
            print("URL " + str(url), "PAGE " + str(page_returned), "TOTAL " + str(total_appearances))
            print(extract_characteristic(url, page_returned, len(list_appearances)))
            dict_entity = extract_characteristic(url, page_returned, total_appearances)
            mongo.insert_mongo(dict_entity, src)
        else:
            if list_appearances != 0:
                content_page_others = get_request(list_appearances[i])
                print(list_appearances[i])
                url_list = list_appearances[i]
                list_appearances_other, total_appearances_others = parse_request(content_page_others, infor_depth)
                print(url_list, content_page_others, total_appearances_others)
                dict_entity = extract_characteristic(url_list, content_page_others, total_appearances_others)
                mongo.insert_mongo(dict_entity, src)
            else:
                print("To access this page is necessary accept storage the cookies")
        i = i + 1
        depth = depth - 1
    return


def set_datetime():
    """
    Generate a timestamp to set in the collection
    :return: str(timestamp)
    """
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string


def extract_characteristic(url_returned, html, total_appearances):
    """
    Extract the tags choose to use in the predict model
    :param url_returned: link used to make scraping
    :param html: the page to find the tags
    :param total_appearances: total of appearances
    :return: a dictionary used to storage in database
    """
    dict_full_characteristic = {}
    soup = BeautifulSoup(html.text, "html.parser")
    list_characteristic = ['p', 'div', 'script', 'img', 'input', 'form', 'href', 'src', 'h1', 'h2']
    dict_full_characteristic['link'] = url_returned
    dict_full_characteristic['total_appearences'] = total_appearances
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
    parser.add_argument("-d", "--depth", help="How many link the function will get in after the first.", type=int,
                        default=15)
    return parser.parse_args()


if __name__ == '__main__':
    args = read_args()
    content_page = get_request(args.url)
    parse_request_wrap(args.url, content_page, args.depth, src=True)
