import time
from ssl import SSLError
import requests
from bs4 import BeautifulSoup
from urllib3.exceptions import MaxRetryError

BACHELORURL = 'https://www.utwente.nl/onderwijs/bachelor/opleidingen/'
MASTERURL = 'https://www.utwente.nl/onderwijs/master/opleidingen/'


def scrape_croho_codes():
    print('Starting scraping process...')

    bachelor_page = requests.get(BACHELORURL)
    master_page = requests.get(MASTERURL)

    print('Getting links for studies...')
    bachelor_soup = BeautifulSoup(bachelor_page.content, 'html.parser')
    master_soup = BeautifulSoup(master_page.content, 'html.parser')
    opleiding_links = list(map(lambda o: o["href"], bachelor_soup.findAll('a', {"class": "programme__link"})))
    opleiding_links.extend(map(lambda o: o["href"], master_soup.findAll('a', {"class": "programme__link"})))

    print('Successfully collected links for studies.')

    croho_codes = []

    print('Attempting to extract CROHO codes from collected links...')

    for link in opleiding_links:
        try:
            page = requests.get(link)
            soup = BeautifulSoup(page.content, 'html.parser')
            croho_element_parent = soup.findAll('div', {"class": "line--crohocode"})[0]
            croho_codes.append(croho_element_parent.findChildren("div", {"class": "line__description"})[0].text)
        except IndexError:
            print('Unable to find element with class line--crohocode on page ' + link)
        except (SSLError, MaxRetryError, requests.exceptions.SSLError):
            print('An error occurred when trying to access ' + link)
        time.sleep(0.5)

    print('Finished extracting CROHO codes from collected links. Found:')
    print(croho_codes)
    return croho_codes
