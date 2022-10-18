"""Common Functions"""


import json
from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError, ConnectionError
from constants import BASE_URL, PROVINCE_KEYWORDS


def get_response(url):
    """Get Response from a URL

    This method receive a url of wikipedia and return a response if the status
    code is 200. Otherwise this method display an error message(invalid url).
    This will also handle the connection error.
    """

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response
        print("Inavlid URL\n")
        return

    except HTTPError:
        print(f"\nBad Status Code {response.status_code}")

    except ConnectionError:
        print(f"\nConnection Error\n")

def parse_countries_urls(html):
    """List of URLs of all countries

    This method receive a response of wikipedia url and return a list of URLs
    of all countries. These urls are the links of wikipedia containing the
    detail of individual country.
    """

    soup = BeautifulSoup(html, 'html.parser')
    spans = soup.find_all('span', class_="flagicon")

    country_url = []
    for span in spans:
        country_url.append(BASE_URL + span.parent.a.get('href'))

    return country_url

def parser_country(html, url, status_code):
    """Parse an html with BeautifulSoup

    This method parse the html page with BeautifulSoup. Here we receive html,
    url of that html page and the status code of that html page. This method
    extract the required information from the html page and return all values
    as a dictionary.
    """
    country = {}
    soup = BeautifulSoup(html, 'html.parser')
    country["name"] = soup.find('span',
                                class_='mw-page-title-main').text
    if country["name"] == "Antarctica":
        return
    td = soup.find('td', class_="infobox-data")
    country["capital"] = td.next_element.text
    country["url"] = url

    province_link = ''
    for key in PROVINCE_KEYWORDS:
        if soup.find('a', text=key) is not None:
            province_link = soup.find('a', text=key).get("href")
            break

    country["province"] = BASE_URL + province_link

    country["response_code"] = str(status_code)

    try:
        coordinates = td.find('span', class_='geo-dec').text.split()
        coordinates = [round(float(i[:-2]), 4) for i in coordinates]
        country["lat_lang"] = coordinates
    except AttributeError:
        country["lat_lang"] = []

    td = soup.find('td', class_="infobox-image") or \
        soup.find('td', class_="infobox-full-data maptable")
    if td is not None:
        imgs = td.find_all('img')

        if len(imgs) >= 2:
            country["Images"] = [
                "https:" + imgs[0].get("src"),
                "https:" + imgs[1].get("src"),
                ]
        else:
            country["Images"] = ["https:" + imgs[0].get("src")]
    else:
        country["Images"] = []

    return country

def get_country_detail(url):
    """Display Country Information

    This method receive an url of wikipedia and get the contents of the link.
    After this it calls the parser_country()function to parse the country
    information. parser_country() returns the country information in as a
    dictionary and finally this method displays the country iinformation in a
    JSON format.
    """

    response = get_response(url)
    
    if response:
        country = parser_country(
                                    response.content,
                                    url,
                                    response.status_code)
        if country is not None:
            json_object = json.dumps(country, indent = 4) 
            print(json_object)
