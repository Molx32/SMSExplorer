# Project
from modules.target.target import Target
from database.database import DatabaseInterface
# Parsing
from html.parser import HTMLParser
import pandas as pd

class ReceiveSMSS(Target):
    
    def __init__(self):
        self.base_url = "https://receive-smss.com"
        self.parser_phone   = ReceiveSMSSParserPhone()
        self.parser_sms     = ReceiveSMSSParserSMS()

        self.phone_urls = []

        # SMS history
        self.sms_history = {}

        # Run the worker
        self.fetch_phones()
        self.fetch_smss()

    def fetch_phones(self):
        r = self.send_request_get(self.base_url)
        self.parser_phone.feed(r.text)
        self.phone_urls = self.parser_phone.get_phones()

    def fetch_smss(self):
        for phone_url in self.phone_urls:
            r = self.send_request_get(self.base_url + phone_url)
            self.parser_sms.feed(r.text)
            smss = self.parser_sms.get_smss()

            # Since we fetch SMSs every X minutes, we'll probably
            # encounter SMS we already handled. For this reason
            # we keep track of the previous SMSs fetched in the
            # self.sms_history attribute.
            # Thus, new SMSs are SMS fetched - SMS we stored in
            # history : 
            # new_smss = set(smss) - self.sms_history[phone_url]
            # self.sms_history[phone_url] = smss

            # Insert new SMSs into database
            # DatabaseInterface.sms_insert()

class ReceiveSMSSParserPhone(HTMLParser):
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.phones         = []
        self.phones_temp    = []

    def get_phones(self):
        self.phones = self.phones_temp
        self.phones_temp = []
        return self.phones
    
    def handle_starttag(self, tag, attrs):
        # We look for <a> tags where attributes are :
        #   - href="/sms/0123456789"
        #   - class="number-boxes1-item-button number-boxess1-item-button button blue stroke rounded tssb "
        # When it's found, add it to the list
        if tag == 'a':
            pair = ("class", "number-boxes1-item-button number-boxess1-item-button button blue stroke rounded tssb ")
            try:
                href = attrs[0]
                classs = attrs[1]
                if classs == pair:
                    self.phones_temp.append(href[1])
            except:
                pass
      
    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass

class ReceiveSMSSParserSMS:

    def __init__(self):
        self.smss       = None
        self.smss_temp  = None
        
    def feed(self, html):
        tables = pd.read_html(html) # Returns list of all tables on page
        self.smss = tables[0]
        for tuple in self.smss.itertuples():
            print(tuple)
        
        self.smss = self.smss_temp
        self.smss_temp = []

    def get_smss(self):
        return self.smss
        pass