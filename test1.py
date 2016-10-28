import urllib2
import itertools


def download(url, num_retries=2):
    print 'Downloading:', url
    try:
        html = urllib2.urlopen(url).read();
    except urllib2.URLError as e:
        print 'Download error', e.reason
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return download(url, num_retries - 1)
    return html


max_error = 5
num_error = 0
for page in itertools.count(1):
    url = 'http://example.webscraping.com/view-%d' % page
    html = download(url)
    if html is None:
        num_error += 1
        if num_error == max_error:
            break
    else:
        num_error = 0
