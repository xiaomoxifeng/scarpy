from pymongo import MongoClient

client = MongoClient('localhost', 27017)
url = 'http://example.webscraping.com/view/United-Kingdom-239'
html = ''
db = client.cache
html = '<p>12345</p>'
db.webpage.insert({'url': url, 'html': html})
db.webpage.find_one(url=url)
