"""Web Scrappper with Multiprocessing"""

from multiprocessing import Pool

from utils import  get_response, parse_countries_urls, display_country_detail


def multiprocessing_countries_detail(start_url):
    """Web Scrappper with Multiprocessing

    This method is used to get information of all countries. In our case there
    are almost 263 links so there will be 26 iterations, 10 URLs will be
    accessed and parsed in a go.
    """

    response = get_response(start_url)
    if response:
        country_urls = parse_countries_urls(response.content)

    with Pool(10) as pool:
        pool.map(display_country_detail, country_urls)
