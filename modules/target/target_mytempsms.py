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
import pandas as pd
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
                Logger.err("Main : " + str(e))
                raise Exception() from e

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
            Logger.err('FETCH SMS - ' + str(e))
            raise Exception('fetch_smss()') from e

    def fetch_instagram(self):
        # Check if message contains website
        for phone_url in self.smss_new: 
            for sms in self.smss_new[phone_url]:
                self.parse_instagram(sms)

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
            Logger.err('POPULATE EXCEPTION - ' + str(num) + ' - ' + str(er))
            raise Exception("populate_database()") from er

class Browser:
    def __init__(self, name, url):
        # Website
        self.name = name
        self.url  = url

        # PARSERS
        # Parser - Instagram
        self.regex_instagram = r"https://ig.me/\w+"

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
            Logger.err('FETCH PHONES - Get countries' + str(e))
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
            Logger.err('FETCH PHONES - Get countries' + str(e))
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
                    sender = tds[0].get_text().replace('\n','')
                    msg = tds[1].get_text().replace('\n','')
                    time_t = tds[2].get_text().replace('\n','')

                if sender and msg and time_t:
                    date    = self.compute_date(time_t)
                    sms     = SMS(sender, receiver.replace('.html', '').split('-')[-1], msg, date, self.compute_country(receiver))
                    Logger.log('Current SMS - ' + str(sms))
                    smss.append(sms)

                    # Parse Instagram
                    # self.parse_instagram(sms)

                    # Reset temporary attributes to None
                    sender  = None
                    msg     = None
                    time_t  = None
            return smss
        except Exception as e:
            Logger.err('PARSE SMS - ' + str(e))
            raise Exception('parse_sms()') from e

    
    def parse_instagram(self, sms):
        # Case 1
        #   "Tap to reset your Instagram p***word: https://ig.me/1ZZOeHuLUwa4Ttq"
        #   There is no username, and it is not necessary to reset the password to access the account
        # Case 2
        #   Instagram link: https://ig.me/r6LPOYK87HRyT73. Don't share it.
        #   Password reset for a given account
        try:
            match = re.findall(self.regex_instagram, sms.msg)
            if match:
                # Get Instagram URL
                url     = match[0]
                source  = self.http_get(url, allow_redirects=False)
                next_url = source.headers['Location']

                # Check if Instagram URL is mobile-oriented
                # instagram://smslogin/?uid=sstisw3&token=3dgsv3&utm_medium=sms&utm_campaign=smslogin&utm_source=instagram&ndid=607dc8ba17346He98c44fc3H607dcd5377618H123
                if 'instagram://smslogin' in next_url:
                    next_url = next_url.replace('instagram://smslogin/', 'https://www.instagram.com/_n/web_smslogin')
                    next_url = next_url.replace('utm_campaign=smslogin', 'utm_campaign=web_smslogin')

                # Parse
                username = "NOT FOUND"
                source  = self.http_get(next_url).text
                soup    = BeautifulSoup(source, features="lxml")
                for span in soup.find_all('span', class_=self.class_username):
                    username = span.get_text()
                    Logger.log('PARSE INSTAGRAM - USERNAME - ' + username)

                # Update SMS                
                sms.add_instagram_account(username)

        except Exception as e:
            sms.add_instagram_account("ERROR")
            Logger.err('EXCEPTION - PARSE INSTAGRAM CALL PATTERN - ' + str(e))
            raise Exception('parse_instagram()') from e