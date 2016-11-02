import threading
import urlparse
import time
import sys
import os
import multiprocessing
from mongo_queue import MongoQueue

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from chapter3.Downloader import Downloader

SLEEP_TIME = 1

def threaded_crawler(seed_url, delay=5, cache=None, scrape_callback=None, user_agent='wswp', proxies=None,
                     num_retries=1, max_threads=10, timeout=60):
    crawl_queue = MongoQueue()
    crawl_queue.clear()
    crawl_queue.push(seed_url)
    D = Downloader(cache=cache, delay=delay, user_agent=user_agent, proxies=proxies, num_retries=num_retries,
                   timeout=timeout)

    def process_queue():
        while True:
            try:
                url = crawl_queue.pop()
            except KeyError:
                # crawl queue is empty
                break
            else:
                html = D(url)
                if scrape_callback:
                    try:
                        links = scrape_callback(url, html) or []
                    except Exception as e:
                        print 'Error in callback for: {}: {}'.format(url, e)
                    else:
                        for link in links:
                            # add this new link to queue
                            crawl_queue.push(normalize(seed_url, link))
                crawl_queue.complete(url)
    threads = []
    while threads or crawl_queue:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
        while len(threads) < max_threads and crawl_queue.peek():
            thread = threading.Thread(target=process_queue)
            # set daemon so main thread can exit when receives ctrl-c
            thread.setDaemon(True)
            thread.start()
            threads.append(thread)
            # time.sleep(SLEEP_TIME)
        time.sleep(SLEEP_TIME)

def process_crawler(args, **kwargs):
    num_cpus = multiprocessing.cpu_count()
    # pool = multiprocessing.Pool(processes=num_cpus)
    print 'Starting {} processes'.format(num_cpus)
    processes = []
    for i in range(num_cpus):
        p = multiprocessing.Process(target=threaded_crawler, args=[args], kwargs=kwargs)
        p.start()
        processes.append(p)
    # wait for processes to complete
    for p in processes:
        p.join()


def normalize(seed_url, link):
    """Normalize this URL by removing hash and adding domain
    """
    link, _ = urlparse.urldefrag(link)  # remove hash to avoid duplicates
    return urlparse.urljoin(seed_url, link)
