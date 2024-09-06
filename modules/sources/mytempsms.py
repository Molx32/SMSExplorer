# System
from datetime import datetime, timedelta
import sys
import re
import time
from io import StringIO

# Project
from database.database import DatabaseInterface
from database.models import SMS
from config.config import Phone
from config.config import Logger
from config.config import Config
# Web
import grequests
import requests
from bs4 import BeautifulSoup

class MyTempSMS:    
    def __init__(self):
        self.base_url = "https://mytempsms.com"
        self.phone_urls = []
        self.phone_nums = []

        self.smss_new = {}
        self.smss_hist= {}

        self.browser = Browser("My Temp SMS", "https://mytempsms.com")

        # Run the worker
        while 1:
            try:
                self.fetch_phones()
                self.fetch_smss()
                self.populate_database()
            except Exception as e:
                raise Exception("Data module - " + str(e))

    def fetch_phones(self):
        # Send request
        self.phone_nums = []
        self.phone_urls = self.browser.fetch_phones()

    def fetch_smss(self):
        try:
            urls = []
            results = grequests.map((grequests.get(self.base_url + u, headers={'User-Agent':'toto'}) for u in self.phone_urls), size=10)
            
            for r in results:
                # Retrieve phone number
                Logger.log("Fetch sms - status code - " + str(r.status_code))
                phone_num = r.request.path_url.split('/')[-1].split('-')[-1].replace('.html','')
                self.phone_nums.append(phone_num)
                Logger.log("Fetch sms - trying to handle - " + str(phone_num))
                smss_temp = self.browser.parse_sms(r)
                Logger.log("Fetch sms - number of sms for " + str(r.request.path_url) + " : " + str(len(smss_temp)))

                try:
                    self.smss_new[phone_num] = [e for e in smss_temp if e not in self.smss_hist[phone_num]]
                except:
                    self.smss_new[phone_num] = smss_temp
                    pass
                self.smss_hist[phone_num] = smss_temp
        except Exception as e:
            raise Exception('fetch_smss()') from e

    def populate_database(self):
        # # Insert new SMSs into database
        try:
            for num in self.phone_nums:
                for sms in self.smss_new[num]:
                    try:
                        DatabaseInterface.sms_insert(sms)
                    except Exception as e:
                        Logger.err('DATABASE EXCEPTION - ' + str(e))
                        raise Exception('sms_insert()') from e
                        continue
        except Exception as er:
            raise Exception("populate_database()") from er

class Browser:
    def __init__(self, name, url):
        # Website
        self.name = name
        self.url  = url

    # PARSERS
    def http_get(self, url, allow_redirects=True):
        headers = {
            'User-Agent':'toto'
        }
        r = requests.get(url, headers=headers, allow_redirects=allow_redirects)
        return r

    def fetch_phones(self):
        try:
            # Fetch countries
            page_num = 1
            countries = set()
            countries_parse = True
            while countries_parse:
                # Get data
                url = 'https://mytempsms.com/receive-sms-online/country.html?page=' + str(page_num)
                source = self.http_get(url).text

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
        except Exception as e:
            raise Exception('fetch_phones() - countries') from e

        try:
            # Fetch phones for each country
            phones = set()
            for country_url in countries:
                if 'upcoming' in country_url or 'foreign' in country_url or 'recently' in country_url:
                    continue
                page_num = 1
                phones_parse = True
                while phones_parse:
                    # Get data
                    url = 'https://mytempsms.com' + country_url.replace('.html', '') + '/page/' + str(page_num) + '.html'
                    source = self.http_get(url).text
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
        except Exception as e:
            raise Exception('fetch_phones() - phones numbers') from e
        
        return list(phones)

    def compute_date(self, date_str):
        date = datetime.now()
        if re.search("[0-9]+ hour", date_str):
            date = date - timedelta(hours=int(date_str.split(' ')[0]))
            return date.strftime("%m/%d/%Y %H:%M:%S")
        if re.match("[0-9]+ minute", date_str):
            date = date - timedelta(minutes=int(date_str.split(' ')[0]))
            return date.strftime("%m/%d/%Y %H:%M:%S")
        if re.match("[0-9]+ second", date_str):
            date = date - timedelta(seconds=int(date_str.split(' ')[0]))
            return date.strftime("%m/%d/%Y %H:%M:%S")
        return date.strftime("%m/%d/%Y %H:%M:%S")
            
    def compute_country(self, receiver):
        for country in Phone.COUNTRIES:
            if receiver.startswith(country['code'].replace('+','')):
                return country['name']

    def parse_sms(self, r):
        try:
            smss = []
            receiver = r.request.path_url
            soup = BeautifulSoup(r.text, features="lxml")
        

            # Initialize next SMS
            sender  = None
            msg     = None
            time_t  = None
            
            # Iterate over all 'div'. Once we retrieved each attribute,
            # we can build a SMS object and reset temporary attributes
            # to None.
            lines = soup.find_all('tr', {'align':''})
            for tr in lines:
                tds = tr.find_all('td')
                if tds:
                    sender  = tds[0].get_text().replace('\n','')
                    msg     = tds[1].get_text().replace('\n','')
                    time_t  = tds[2].get_text().replace('\n','')

                if sender and msg and time_t:
                    date    = self.compute_date(time_t)
                    sms     = SMS(None, sender, receiver.replace('.html', '').split('-')[-1], msg, date, self.compute_country(receiver))
                    Logger.log('Current SMS - ' + str(sms))
                    smss.append(sms)

                    # Reset temporary attributes to None
                    sender  = None
                    msg     = None
                    time_t  = None
            return smss
        except Exception as e:
            raise Exception('parse_sms()') from e
