"""Web Scrappper with Asyncio"""

import asyncio
import aiohttp
import json
from requests.exceptions import HTTPError, ConnectionError
from utils import parser_country, parse_countries_urls


async def get_response(session, url):
    """Get Response from a URL

    This method receive a session and url of wikipedia and return a response.
    This will also handle the connection error and HTTPError.
    """

    try:
        async with session.get(url, ssl=False) as response:
            return {
                    "url": url,
                    "status_code": response.status,
                    "response_text": await response.text()
                    }

    except HTTPError:
        print(f"\nBad Status Code {response.status}")

    except ConnectionError:
        print(f"\nConnection Error\n")

async def get_country_detail(session, url):
    """Coroutine method to get data from url

    This method is a coroutine. This should be called by asyncio. This function
    receive a session and url. First, it calls get_response() and wait for
    response. When a response is returned by get_response() it sends this
    response to parser to extract the required information from the html page.
    And finally print the result of parser() in JSON format.
    """
    response = await get_response(session, url)
    country = parser_country(response["response_text"],
                             response["url"],
                             response["status_code"])
    if country is not None:
        json_object = json.dumps(country, indent = 4) 
        print(json_object)

async def async_countries_detail(start_url):
    """Asynchronous approac for web crawler of countries
    
    This method will receive a Starting Url of Wikipedia and the extract all
    the urls of all countries. Then this function get response from these urls
    asynchronously using asyncio and aiohttp.
    """
    async with aiohttp.ClientSession() as session:
        response = await get_response(session, start_url)
        if response:
            country_urls = parse_countries_urls(response["response_text"])
        tasks = []
        for url in country_urls:
            task = asyncio.create_task(get_country_detail(session, url))
            tasks.append(task)
        await asyncio.gather(*tasks)
