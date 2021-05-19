import requests
from bs4 import BeautifulSoup


def get_request(url_request):
    return requests.get(url_request)


def parse_request(page_returned):
    """

    :param page_returned: It have the main link requested
    :return: List of links found
    """
    list_appearances = []
    soup = BeautifulSoup(page_returned.text, "html.parser")
    print("The href links are :")
    for link in soup.select('a[href^="http"]'):
        print(link.get('href'))
        list_appearances.append(link.get('href'))
    return list_appearances


def extract_characteristic(html):
    soup = BeautifulSoup(html.text, "html.parser")
    list_characteristic = ['p', 'div', 'script','img','input','form','href','src','h1','h2']
    dict_full_characteristic={}
    for i in list_characteristic:
        dict_full_characteristic[f'{i}'] = len(soup.find_all(f'{i}'))
    return dict_full_characteristic



def save_db():
    pass

# implementing search and save in database
# implementing API
# implementign randon forest 100 tree of 10 deph

if __name__ == '__main__':
    url = "https://en.wikipedia.org/wiki/Algorithm"
    content_page = get_request(url)
    print(parse_request(content_page))
    print(extract_characteristic(content_page))

