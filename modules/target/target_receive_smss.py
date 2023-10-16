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
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService

class ReceiveSMSS:    
    def __init__(self):
        self.base_url = "https://receive-smss.com"
        self.phone_urls     = []

        self.smss_new = {}
        self.smss_hist= {}

        self.browser        = Browser("Receive SMSs", "https://receive-smss.com")

        # Run the worker
        while 1:
            try:
                self.fetch_phones()
                self.fetch_smss()
                self.fetch_instagram()

                self.populate_database()
            except Exception as e:
                print("Main : " + str(e))

    def fetch_phones(self):
        # Send request
        self.phone_urls = self.browser.fetch_phones()

    def fetch_smss(self):
        for phone_url in self.phone_urls:
            # start = time.time()
            smss_temp = self.browser.fetch_smss(phone_url)
            # end = time.time()
            # Logger.log('INNER - FETCH SMSS FOR ' + phone_url + ' - ' + str(end - start))

            # Since we fetch SMSs every X minutes, we'll probably
            # encounter SMS we already handled. For this reason
            # we keep track of the previous SMSs fetched in the
            # self.smss_hist attribute.
            # Thus, new SMSs are SMS fetched - SMS we stored in
            # history:
            try:
                self.smss_new[phone_url] = [e for e in smss_temp if e not in self.smss_hist[phone_url]]
            except:
                self.smss_new[phone_url] = smss_temp
                pass
            self.smss_hist[phone_url] = smss_temp

    def fetch_instagram(self):
        # Check if message contains website
        Logger.log('FETCH INSTAGRAM CALL - ' + str(len(self.smss_new)))
        for phone_url in self.smss_new: 
            for sms in self.smss_new[phone_url]:
                self.parse_instagram(sms)

    def populate_database(self):
        # # Insert new SMSs into database
        for phone_url in self.phone_urls:
            try:
                start = time.time()
                for sms in self.smss_new[phone_url]:
                    print("insert")
                    DatabaseInterface.sms_insert(sms)
                end = time.time()
                Logger.log('DATABASE ADD - ' + phone_url + ' - ' + str(end - start))
            except Exception as e:
                Logger.log('DATABASE EXCEPTION - ' + phone_url + ' - ' + str(e))
                continue

    def parse_instagram(self, sms):
        # Case 1
        #   "Tap to reset your Instagram p***word: https://ig.me/1ZZOeHuLUwa4Ttq"
        #   There is no username, and it is not necessary to reset the password to access the account
        # Case 2
        #   Instagram link: https://ig.me/r6LPOYK87HRyT73. Don't share it.
        #   Password reset for a given account
        try:
            regex = r"https://ig.me/\w+"
            l = re.findall(regex, sms.msg)
            if l:
                Logger.log('PARSE INSTAGRAM CALL PATTERN - ' + str(l[0]))
                # Parse
                url = l[0]
                r = self.browser.parse_instagram(url)
                sms.add_instagram_account(r)
        except Exception as e:
            Logger.log('EXCEPTION - PARSE INSTAGRAM CALL PATTERN - ' + str(e))

class Browser:
    def __init__(self, name, url):
        # Website
        self.name = name
        self.url  = url
        # FIREFOX
        # Source : https://takac.dev/example-of-selenium-with-python-on-docker-with-latest-firefox/
        #
        # Set Firefox profile
        PROFILE = webdriver.FirefoxProfile()
        PROFILE.set_preference("browser.cache.disk.enable", True)
        PROFILE.set_preference("browser.cache.memory.enable", True)
        PROFILE.set_preference("browser.cache.offline.enable", False)
        PROFILE.set_preference("permissions.default.stylesheet", 2)
        PROFILE.set_preference("permissions.default.image", 2)
        PROFILE.set_preference("network.http.use-cache", False)
        PROFILE.set_preference("general.useragent.override","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:72.0) Gecko/20100101 Firefox/72.0")
        # FireFox Options
        FIREFOX_OPTS = Options()
        # FIREFOX_OPTS.log.level = "trace"    # Debug
        FIREFOX_OPTS.headless = True
        FIREFOX_OPTS.profile = PROFILE
        # Instanciate browser
        self.browser = webdriver.Firefox(options=FIREFOX_OPTS)

        # Parsers

        # Data
        self.class_a    = "number-boxes1-item-button number-boxess1-item-button button blue stroke rounded tssb"
        self.class_username = "x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xl565be x1s688f x5n08af x1tu3fi x3x7a5m x10wh9bi x1wdrske x8viiok x18hxmgj"

        self.class_sender = "col-md-3 sender"
        self.class_msg    = "col-md-6 msg"
        self.class_time   = "col-md-3 time"
        self.smss = []

    def fetch_phones(self):
        # Fetch
        phone_urls = []
        self.browser.get(self.url)

        # Parse
        soup = BeautifulSoup(self.browser.page_source, features="lxml")
        for a in soup.find_all('a'):
            try:
                classes = a.get('class')
                if not classes:
                    continue

                if self.class_a in " ".join(classes):
                    sender = a.get('href')
                    phone_urls.append(sender)
            except Exception as e:
                print("Browser fetch phone : " + str(e))

        return phone_urls

    def fetch_smss(self, receiver):
        try:
            smss = []
            phone_url = self.url + receiver
            start = time.time()
            self.browser.get(phone_url)
            end = time.time()
            Logger.log('FETCH AND PARSE - SELENIUM GET PAGE - ' + str(end - start))
        except Exception as e:
            print("BROWSER GET" + str(e))

        try:
            start = time.time()
            soup = BeautifulSoup(self.browser.page_source, features="lxml")
            end = time.time()
            Logger.log('FETCH AND PARSE - INSTANCIATE BEAUTIFUL SOUP - ' + str(end - start))
        except Exception as e:
            print("BEAUTIFUL SOUP" + str(e))

        # Initialize next SMS
        sender  = None
        msg     = None
        time_t  = None
        
        start = time.time()
        # Iterate over all 'div'. Once we retrieved each attribute,
        # we can build a SMS object and reset temporary attributes
        # to None.
        for div in soup.find_all('div'):
            try:
                if self.class_sender in " ".join(div.get('class')):
                    sender = div.get_text().replace("Sender",'')
                if self.class_msg in " ".join(div.get('class')):
                    msg = div.get_text().replace("Message",'').replace('\n','')
                if self.class_time in " ".join(div.get('class')):
                    time_t = div.get_text().replace("Time",'')
            except:
                pass
            
            if sender and msg and time_t:
                date    = self.compute_date(time_t)
                sms     = SMS(sender, receiver, msg, date, self.compute_country(receiver))
                smss.append(sms)

                # Reset temporary attributes to None
                sender  = None
                msg     = None
                time_t    = None
        end = time.time()
        Logger.log('FETCH AND PARSE - GET DATA - ' + str(end - start))

        return smss
                    
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

    def parse_instagram(self, url):
        try:
            self.browser.get(url)

            # Parse
            soup = BeautifulSoup(self.browser.page_source, features="lxml")
            for span in soup.find_all('span'):
                if self.class_username in " ".join(span.get('class')):
                    username = span.get_text()
                    Logger.log('PARSE INSTAGRAM - USERNAME - ' + username)
                    return username
            return "NOT FOUND"
        except Exception as e:
            Logger.log("PARSE INSTAGRAM - USERNAME - " + str(e))