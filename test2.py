#coding=utf-8
import Queue
import re
import robotparser
import urlparse

from chapter3.Downloader import Downloader


def link_crawler(seed_url, user_agent='json', delay=5, max_depth=-1, max_urls=-1, headers=None, link_regex=None,
                 num_retries=1,
                 proxy=None, scrape_callback=None,cache=None):
    crawl_queue = Queue.deque([seed_url])
    seen = {seed_url: 0}
    num_urls = 0
    rp = get_robots(seed_url)
    D = Downloader(delay=delay, user_agent=user_agent, proxies=proxy, num_retries=num_retries, cache=cache)
    while crawl_queue:
        url = crawl_queue.pop()
        depth = seen[url]
        if rp.can_fetch(user_agent, url):
            html = D(url)
            links = []
            if scrape_callback:
                links.extend(scrape_callback(url, html) or [])
            if depth != max_depth:
                if link_regex:
                    links.extend(link for link in get_links(html) if re.match(link_regex, link))
                for link in links:
                    link = normalize(seed_url, link)
                    #去重
                    if link not in seen:
                        seen[link] = depth + 1
                        if same_domain(seed_url, link):
                            # success! add this new link to queue
                            crawl_queue.append(link)
            num_urls += 1
            if num_urls == max_urls:
                break
        else:
            print 'Blocked by robots.txt', url


def normalize(seed_url, link):
    link, _ = urlparse.urldefrag(link)
    return urlparse.urljoin(seed_url, link)

def same_domain(url1, url2):
    return urlparse.urlparse(url1).netloc == urlparse.urlparse(url2).netloc


def get_links(html):
    #
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webpage_regex.findall(html)


def get_robots(url):
    """Initialize robots parser for this domain
    """
    rp = robotparser.RobotFileParser()
    rp.set_url(urlparse.urljoin(url, '/robots.txt'))
    rp.read()
    return rp



if __name__ == '__main__':
    link_crawler('http://example.webscraping.com', user_agent='GoodCrawler', delay=0,
                 link_regex='/(index|view)', max_depth=1,
                 num_retries=1)
