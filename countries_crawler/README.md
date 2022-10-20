# Website Crawler
Make a crawler for getting information of the countries using
URL: https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_area

Here we are comparing the following 4 approaches to parse the information of the country:
- Simple
- Concurrent Future
- Asyncio
- Multiprocessing
#### **How to run**
- Clone the repository `https://github.com/Zain-Bajwa/country_crawler.git`
- Create virtual environment
```bash
$ python -m venv .venv
$ source .venv/bin/activate
```
- $ Install `requirements.txt`
```bash
$ pip install requirements.txt
```
- Run `crawler_main.py`
```bash
$ python crawler_main.py
```
Make sure you have an internet connection. By the end of the task, you can see the time consumed by all approaches individually.
