"""Web Scrappper with Threading"""

import asyncio
import aiohttp
import json
from threading import Thread
from requests.exceptions import HTTPError, ConnectionError
from utils import parser_country, parse_countries_urls, get_response


async def async_get_response(session, url):
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
    response = await async_get_response(session, url)
    country = parser_country(response["response_text"],
                             response["url"],
                             response["status_code"])
    if country is not None:
        json_object = json.dumps(country, indent = 4) 
        print(json_object)


async def async_(country_urls):
    """Asynchronous approac for web crawler of countries
    
    This method will receive a Starting Url of Wikipedia and the extract all
    the urls of all countries. Then this function get response from these urls
    asynchronously using asyncio and aiohttp.
    """
    async with aiohttp.ClientSession() as session:
        tasks = []
        
        for url in country_urls:
            task = asyncio.create_task(get_country_detail(session, url))
            tasks.append(task)
        await asyncio.gather(*tasks)


def threading_countries_detail(start_url):
    """Asynchronous approac for web crawler of countries
    
    This method will receive a Starting Url of Wikipedia and the extract all
    the urls of all countries. Then this function get response from these urls
    asynchronously using asyncio and aiohttp.
    """
    response = get_response(start_url)
    if response:
        country_urls = parse_countries_urls(response.content)
    t1 = Thread(target=asyncio.run(async_), args=(country_urls[0:10],))
    # t2 = Thread(target=asyncio.run(async_), args=(country_urls[10:11],))
    t1.start()
    t1.join()
