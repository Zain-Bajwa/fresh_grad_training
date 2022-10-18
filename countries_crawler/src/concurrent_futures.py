"""Web Scrappper with Concurrent Futures"""


import concurrent.futures as cf
from constants import NUM_THREADS
from utils import  get_response, parse_countries_urls, get_country_detail
    

def concurrent_countries_detail(start_url):
    """Web Scrappper with Multiprocessing

    This method is used to get information of all countries. In our case there
    are almost 263 links so there will be 26 iterations, 10 URLs will be
    accessed and parsed in a go.
    """

    response = get_response(start_url)
    if response:
        country_urls = parse_countries_urls(response.content)
   
    with cf.ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        executor.map(get_country_detail, country_urls)
