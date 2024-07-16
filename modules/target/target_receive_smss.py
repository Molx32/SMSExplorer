# System
from datetime import datetime, timedelta
import sys
import re
import time
import uuid

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

class ReceiveSMSS:    
    def __init__(self):
        self.base_url = "https://receive-smss.com"
        self.user_agent = None
        self.phone_urls = []
        self.phone_nums = []

        self.smss_new = {}
        self.smss_hist= {}

        self.browser = Browser("Receive SMSs", "https://receive-smss.com")

        # Run the worker
        while 1:
            try:
                self.randomize_user_agent()
                start = time.time()
                self.fetch_phones()
                self.fetch_smss()
                self.populate_database()
                end = time.time()
                Logger.log('MAIN - ' + str(end - start))
            except Exception as e:
                raise Exception('MAIN') from e
                continue

    def randomize_user_agent(self):
        self.user_agent = str(uuid.uuid4())

    def fetch_phones(self):
        try:
            # Send request
            self.phone_urls = self.browser.fetch_phones()
            for phone_url in self.phone_urls:
                self.phone_nums.append(phone_url.split('/')[-2])
        except Exception as e:
            raise Exception('ReceiveSMSS - fetch_phones()') from e

    def fetch_smss(self):
        # Send all parallel requests
        headers = {'User-Agent': self.user_agent}
        results = grequests.map((grequests.get(self.base_url + u, headers=headers) for u in self.phone_urls), size=5)

        # Handle all results
        try:
            Logger.log('ReceiveSMSS - fetch_smss' + self.user_agent)
            for result in results:
                # Get phone number
                # and parse all results
                DatabaseInterface.log(result)
                phone_num = result.request.path_url.split('/')[-2]
                smss_temp = self.browser.parse_sms(result)

                # For each SMS, check if it is in history.
                if phone_num in self.smss_hist.keys():
                    self.smss_new[phone_num] = [e for e in smss_temp if e not in self.smss_hist[phone_num]]
                else:
                    self.smss_new[phone_num] = smss_temp
                self.smss_hist[phone_num] = smss_temp
        except Exception as e:
            raise Exception('Receive SMS - fetch_smss()') from e

    def populate_database(self):
        try:
            # Insert new SMSs into database
            Logger.log('ReceiveSMSS - populate_database')
            for phone_url in self.phone_urls:
                phone_num = phone_url.split('/')[-2]
                for sms in self.smss_new[phone_num]:
                    DatabaseInterface.sms_insert(sms)
        except Exception as e:
            raise Exception('ReceiveSMSS - populate_database()') from e

class Browser:
    def __init__(self, name, url):
        # Website
        self.name = name
        self.url  = url

        # Data
        self.class_a    = "number-boxes1-item-button number-boxess1-item-button button blue stroke rounded tssb"
        self.class_username = "x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xl565be x1s688f x5n08af x1tu3fi x3x7a5m x10wh9bi x1wdrske x8viiok x18hxmgj"

        self.class_sender = "col-md-3 sender"
        self.class_msg    = "col-md-6 msg"
        self.class_time   = "col-md-3 time"
        self.smss = []

    def http_get(self, url, allow_redirects=True):
        Logger.log('Browser - http_get')
        headers = {
            'User-Agent': str(uuid.uuid4())
        }
        r = requests.get(url, headers=headers, allow_redirects=allow_redirects)
        DatabaseInterface.log(r)
        return r

    def fetch_phones(self):
        Logger.log('Browser - fetch_phones')
        # Fetch
        phone_urls = []
        source = self.http_get(self.url).text

        # Parse
        soup = BeautifulSoup(source, features="lxml")
        for a in soup.find_all('a', class_=self.class_a):
            try:
                sender = a.get('href')
                phone_urls.append(sender)
            except Exception as e:
                raise Exception('fetch_phones') from e

        return phone_urls

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
        Logger.log('Browser - compute_country')
        for country in Phone.COUNTRIES:
            if receiver.startswith(country['code'].replace('+','')):
                return country['name']

    def parse_sms(self, r):
        Logger.log('Browser - parse_sms')
        try:
            smss = []
            receiver = r.request.path_url
            soup = BeautifulSoup(r.text, features="lxml")
        except Exception as e:
            raise Exception('fetch_phones') from e

        # Initialize next SMS
        sender  = None
        msg     = None
        time_t  = None
        
        # Find country
        country = soup.find('title').get_text().split('|')[-1].replace(' Phone Number', '').strip()

        # Iterate over all 'div'. Once we retrieved each attribute,
        # we can build a SMS object and reset temporary attributes
        # to None.
        for div in soup.find_all('div'):
            try:
                if self.class_sender in " ".join(div.get('class')):
                    sender = div.get_text().replace("Sender",'')
                if self.class_msg in " ".join(div.get('class')):
                    msg = div.get_text().replace("Message",'')
                    msg = sanitize_msg(msg)
                if self.class_time in " ".join(div.get('class')):
                    time_t = div.get_text().replace("Time",'')
            except:
                pass
            
            if sender and msg and time_t:
                date    = self.compute_date(time_t)
                sms     = SMS(sender, receiver, msg, date, country)
                smss.append(sms)

                # Reset temporary attributes to None
                sender  = None
                msg     = None
                time_t    = None

        return smss
    
    def sanitize_msg(self, msg):
        msg = msg.replace('\n',' ')
        msg = msg.replace('***word', 'assword')
        msg = msg.replace('iden***y', 'identity')
        msg = msg.replace('do***ent', 'document')
        return msg
