"""Website Crawler"""

import asyncio
import time
from simple import simple_countries_detail
from asyncio_gather import async_countries_detail
from multiprocessing_ import multiprocessing_countries_detail
from concurrent_futures import concurrent_countries_detail
from threading_ import threading_countries_detail
from constants import START_URL


def main():
    """Main Function"""

    time_list = []

    # Web Scrappper with Simple Approach
    start_time = time.time()
    simple_countries_detail(START_URL)
    time_list.append("Time consumed in simple approach: "
                           + str(round(time.time() - start_time, 2))
                           + "s")

    # Web Scrappper with Asyncio
    start_time = time.time()
    asyncio.run(async_countries_detail(START_URL))
    time_list.append("Time consumed in asyncio approach: "
                           + str(round(time.time() - start_time, 2))
                           + "s")

    # Web Scrappper with Multiprocessing
    start_time = time.time()
    multiprocessing_countries_detail(START_URL)
    time_list.append("Time consumed in multiprocessing approach: "
                           + str(round(time.time() - start_time, 2))
                           + "s")

    # Web Scrappper with Concurrent Futures
    start_time = time.time()
    concurrent_countries_detail(START_URL)
    time_list.append("Time consumed in multiprocessing approach: "
                           + str(round(time.time() - start_time, 2))
                           + "s")

    # # Web Scrappper with Threading
    # start_time = time.time()
    # threading_countries_detail(START_URL)
    # print(
    #     f"Time consumed in multiprocessing approach: "
    #     f"{round(time.time() - start_time, 2)}s"
    #     )

    for time_ in time_list:
        print(time_)


if __name__ == "__main__":
    main()
