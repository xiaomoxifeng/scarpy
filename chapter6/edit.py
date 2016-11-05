# -*- coding: utf-8 -*-

import urllib
import urllib2
import mechanize
import login

COUNTRY_URL = 'http://example.webscraping.com/edit/United-Kingdom-239'
def mechanize_edit():
    #login
    br = mechanize.Browser()
    br.open(login.LOGIN_URL)
    br.select_form(nr=0)
    print br.form
    br['email'] = login.LOGIN_EMAIL
    br['password']=login.LOGIN_PASSWORD
    response = br.submit()

    #edit
    br.open(COUNTRY_URL)
    br.select_form(nr=0)
    print 'Population before: ',br['population']
    br['population']=str(int(br['population'])+1)
    br.submit()

    #check
    br.open(COUNTRY_URL)
    br.select_form(nr =0)
    print 'population after :', br['population']

if __name__ == '__main__':
    mechanize_edit()