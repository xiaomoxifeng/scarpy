import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from threaded_crawler import threaded_crawler
from chapter3.MongoCache import MongoCache
from alexa_cb import AlexaCallback


def main(max_threads):
    scrape_callback = AlexaCallback()
    cache = MongoCache()
    threaded_crawler(scrape_callback.seed_url,
                     scrape_callback=scrape_callback,
                     cache=cache, max_threads=max_threads,
                     timeout=10)


if __name__ == '__main__':
    max_threads = int(sys.argv[1])
    main(max_threads)
