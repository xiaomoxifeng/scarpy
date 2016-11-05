import urllib
import urllib2
import glob
import sqlite3
import os
import cookielib
import json
import time
import lxml.html

LOGIN_EMAIL = 'example@webscraping.com'
LOGIN_PASSWORD = 'example'
LOGIN_URL = 'http://example.webscraping.com/user/login'


def parse_form(html):
    """extract all input properties from the form
    """
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    return data



# def load_ff_sessions(session_filename):
#     cj = cookielib.CookieJar()
#     if os.path.exists(session_filename):
#         try:
#             json_data = json.loads(open(session_filename, 'rb').read())
#         except ValueError as e:
#             print 'Error parsing session JSON:', str(e)
#         else:
#             for window in json_data.get('windows', []):
#                 for cookie in window.get('cookies', []):
#                     import pprint; pprint.pprint(cookie)
#                     c = cookielib.Cookie(0, cookie.get('name', ''), cookie.get('value', ''),
#                         None, False,
#                         cookie.get('host', ''), cookie.get('host', '').startswith('.'), cookie.get('host', '').startswith('.'),
#                         cookie.get('path', ''), False,
#                         False, str(int(time.time()) + 3600 * 24 * 7), False,
#                         None, None, {})
#                     cj.set_cookie(c)
#     else:
#         print 'Session filename does not exist:', session_filename
#     return cj
#
#
# def find_ff_sessions():
#     paths = [
#         '~/.mozilla/firefox/*.default',
#         '~/Library/Application Support/Firefox/Profiles/*.default',
#         '%APPDATA%/Roaming/Mozilla/Firefox/Profiles/*.default'
#     ]
#     for path in paths:
#         filename = os.path.join(path, 'sessionstore.js')
#         matches = glob.glob(os.path.expanduser(filename))
#         if matches:
#             return matches[0]
def login_cookies():
    """working login
    """
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    html = opener.open(LOGIN_URL).read()
    data = parse_form(html)
    data['email'] = LOGIN_EMAIL
    data['password'] = LOGIN_PASSWORD
    encoded_data = urllib.urlencode(data)
    request = urllib2.Request(LOGIN_URL, encoded_data)
    response = opener.open(request)
    print response.geturl()
    return opener
if __name__ == '__main__':
    login_cookies()
