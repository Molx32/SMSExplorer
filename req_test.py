import grequests
import requests
import time
import json
from bs4 import BeautifulSoup
import re

def http_get(url, allow_redirects=True):
    headers = {
        'User-Agent':'toto'
    }
    r = requests.get(url, headers=headers, allow_redirects=allow_redirects)
    return r

def fetch_phones():
    countries = set()

    # Fetch countries
    page_num = 1
    countries_parse = True
    while countries_parse:
        # Get data
        url = 'https://mytempsms.com/receive-sms-online/country.html?page=' + str(page_num)
        source = http_get(url).text

        # Parse
        soup = BeautifulSoup(source, features="lxml")
        links = soup.find_all('a', {'href': re.compile(r"/receive-sms-online/.+-phone-number.html")})

        countries_len = len(countries)
        for a in links:
            countries.add(a.get('href'))

        if countries_len == len(countries):
            countries_parse = False

        # Increment page num
        page_num = page_num + 1


    # Fetch phones for each country
    for country_url in countries:
        page_num = 1
        phones = set()
        phones_parse = True
        while phones_parse:
            # Get data
            url = 'https://mytempsms.com' + country_url + '/page/' + str(page_num) + '.html'
            source = http_get(url).text
            # Parse
            # https://mytempsms.com/receive-sms-online/france-phone-number-6822097181.html
            country_path = country_url.replace('.html', '')
            soup = BeautifulSoup(source, features="lxml")
            links = soup.find_all('a', {'href': re.compile(country_path+"-[0-9]+.html")})
            phones_len = len(phones)
            for a in links:
                phones.add(a.get('href'))

            if phones_len == len(phones):
                phones_parse = False

            # Increment page num
            page_num = page_num + 1

        for p in phones:
            print(p)



r = http_get('https://mytempsms.com/receive-sms-online/france-phone-number-4589532415.html')
soup = BeautifulSoup(r.text, features="lxml")

# Iterate over all 'div'. Once we retrieved each attribute,
# we can build a SMS object and reset temporary attributes
# to None.
lines = soup.find_all('tr', {'align':''})

print('PARSE')
for tr in lines:
    tds = tr.find_all('td')
    if tds:
        sender = tds[0].get_text().replace('\n','')
        msg = tds[1].get_text().replace('\n','')
        time_ts = tds[2].get_text().replace('\n','')

        print(sender)
        print(msg)
        print(time_ts)