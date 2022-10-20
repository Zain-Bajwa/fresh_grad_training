"""Common Functions"""


import json

from bs4 import BeautifulSoup
import requests

from constants import BASE_URL, PROVINCE_KEYWORDS


def get_response(url):
    """Get Response from a URL

    This method receive a url of wikipedia and return a response if the status
    code is 200. Otherwise this method display an error message(invalid url).
    This will also handle the connection error.
    """

    response = requests.get(url)
    if response.ok:
        return response
    print(f"\nInavlid URL or Bad Status Code {response.status_code}")
    return None


def parse_countries_urls(html_content):
    """List of URLs of all countries

    This method receive a response of wikipedia url and return a list of URLs
    of all countries. These urls are the links of wikipedia containing the
    detail of individual country.
    """

    soup = BeautifulSoup(html_content, "html.parser")
    country_urls_spans = soup.select("span.flagicon")

    country_urls = [BASE_URL + url_span.parent.a.get("href")
                        for url_span in country_urls_spans]
    return country_urls


def parser_country(html_content, url, status_code):
    """Parse an html with BeautifulSoup

    This method parse the html page with BeautifulSoup. Here we receive html,
    url of that html page and the status code of that html page. This method
    extract the required information from the html page and return all values
    as a dictionary.
    """
    country = {}
    soup = BeautifulSoup(html_content, "html.parser")
    country["name"] = soup.select_one(".mw-page-title-main").text
    if country["name"] == "Antarctica":
        return ""
    country_detail_td = soup.select_one("td.infobox-data")
    country["capital"] = country_detail_td.next_element.text
    country["url"] = url

    country["province"] = [
        BASE_URL + soup.select_one(f"a:-soup-contains('{key}')").get("href")
        for key in PROVINCE_KEYWORDS
        if soup.select_one(f"a:-soup-contains('{key}')") is not None
    ]

    country["response_code"] = str(status_code)

    if country_detail_td.select_one("span.geo-dec") is not None:
        coordinates = country_detail_td.select_one("span.geo-dec").text.split()
        coordinates = [round(float(i[:-2]), 4) for i in coordinates]
        country["lat_lang"] = coordinates
    else:
        country["lat_lang"] = []

    flag_images_img = soup.select(
        ".infobox-image img, .infobox-full-data.maptable img"
    )
    country["Images"] = [
        "https:" + flag_link.get("src") for flag_link in flag_images_img
    ]
    return country


def display_country_detail(url):
    """Display Country Information

    This method receive an url of wikipedia and get the contents of the link.
    After this it calls the parser_country()function to parse the country
    information. parser_country() returns the country information in as a
    dictionary and finally this method displays the country iinformation in a
    JSON format.
    """

    response = get_response(url)

    if response:
        country = parser_country(response.content, url, response.status_code)
        print(json.dumps(country, indent=4))
