# System
from datetime import datetime, timedelta
import sys
import re
import time
from io import StringIO



# Project
from modules.target.target import Target
from database.database import DatabaseInterface
from database.models import SMS
# Parsing
from html.parser import HTMLParser
import pandas as pd

class ReceiveSMSS(Target):    
    def __init__(self):
        self.base_url = "https://receive-smss.com"
        self.parser_phone   = ReceiveSMSSParserPhone()
        self.parser_sms     = ReceiveSMSSParserSMS()
        self.phone_urls = []

        # Run the worker
        while 1:
            self.fetch_phones()
            self.fetch_smss()

    def fetch_phones(self):
        # Send request
        r = self.send_request_get(self.base_url)
        # Analyse and get phones
        self.parser_phone.feed(r.text)
        self.phone_urls = self.parser_phone.get_phones()

    def fetch_smss(self):
        for phone_url in self.phone_urls:
            # Send request
            r = self.send_request_get(self.base_url + phone_url)
            # Analyse and get SMSs
            self.parser_sms.feed(r.text, phone_url)
            smss = self.parser_sms.get_smss(phone_url)

            # Check if message contains website

            # Insert new SMSs into database
            for sms in smss:
                try:
                    DatabaseInterface.sms_insert(sms)
                except:
                    print("EXCEPTION")
                    time.sleep(5)
                    continue

class ReceiveSMSSParserPhone(HTMLParser):
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.phones         = set()
        self.phones_temp    = set()

    def get_phones(self):
        self.phones = self.phones_temp
        self.phones_temp = set()
        return list(self.phones)
    
    def handle_starttag(self, tag, attrs):
        # We look for <a> tags where attributes are :
        #   - href="/sms/0123456789"
        #   - class="number-boxes1-item-button number-boxess1-item-button button blue stroke rounded tssb "
        # When it's found, add it to the list
        pair = ("class", "number-boxes1-item-button number-boxess1-item-button button blue stroke rounded tssb ")
        if tag == 'a':
            try:
                href = attrs[0]
                classs = attrs[1]
                if classs == pair:
                    self.phones_temp.add(href[1])
            except:
                pass
      
    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass

class ReceiveSMSSParserSMS:

    def __init__(self):
        self.smss_hist  = {}
        self.smss_new   = {}
        self.smss_temp  = {}
        
    def feed(self, html, receiver_url):
        # Reset SMS list
        self.smss_new[receiver_url]   = []
        self.smss_temp[receiver_url]  = []

        # Get new SMSs and populate list
        table = pd.read_html(StringIO(html))[0]
        for tuple in table.itertuples():
            sender      = tuple[1]
            msg         = tuple[2]
            date        = self.compute_date(tuple[3])
            receiver    = receiver_url.split('/')[-2]
            
            # Add SMS to temp list
            sms = SMS(sender, receiver, msg, date)
            self.smss_temp[receiver_url].append(sms)

        # Since we fetch SMSs every X minutes, we'll probably
        # encounter SMS we already handled. For this reason
        # we keep track of the previous SMSs fetched in the
        # self.smss_hist attribute.
        # Thus, new SMSs are SMS fetched - SMS we stored in
        # history:
        try:
            self.smss_new[receiver_url] = [e for e in self.smss_temp[receiver_url] if e not in self.smss_hist[receiver_url]]
        except:
            self.smss_new[receiver_url] = self.smss_temp[receiver_url]
            pass
        self.smss_hist[receiver_url] = self.smss_temp[receiver_url]

    def get_smss(self, receiver_url):
        return self.smss_new[receiver_url]

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