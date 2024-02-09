# System
from datetime import datetime, timedelta
import sys
import json
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
import requests
import pandas as pd
import requests
from bs4 import BeautifulSoup

class DataModule:    
    def __init__(self, name, base_url):
        self.name       = name
        self.base_url   = base_url
        self.smss       = []

        self.run()

    def run(self):
        # Run the worker
        try:
            # Get data
            self.smss = DatabaseInterface.get_sms_by_url(self.base_url)
            if self.smss:
                Logger.log('1DATA - ' + self.name + str(self.smss))
                for sms in self.smss:
                    Logger.log('2DATA - ' + self.name + str(sms))
                    #DATA - Mock - run - 'Mock' object has no attribute 'data'
                    sms_id  = sms[0]
                    url     = sms[1]
                    data    = self.retrieve_data(url)
                    Logger.log('3DATA - ' + self.name + str(data))
                    self.populate_database(sms_id, data)

        except Exception as e:
            Logger.log('DATA - ' + self.name + ' - run - ' + str(e))

    def populate_database(self, sms_id, data):
        try:
            # Insert new SMSs into database
            DatabaseInterface.sms_data_insert(sms_id, data)
        except Exception as e:
            Logger.log('DATA - ' + self.name + ' - populate_database - ' + str(e))

    def retrieve_data(self, url):
        return None



class Earnrwds(DataModule):
    def __init__(self):
        name        = 'Earnrwds'
        base_url    = 'https://earnrwds.com/'
        super().__init__(name, base_url)
    
    def retrieve_data(self, url):
        # Get additional data
        data = {}
        resp = requests.get(url, allow_redirects=False, verify=False)
        redirect_url = resp.headers['Location']
        if redirect_url:
            params = redirect_url.split('?')[1]
            for param in params.split('&'):
                key = param.split('=')[0]
                val = param.split('=')[1]
                data[key] = val
        
            json_data = json.dumps(data,ensure_ascii=False)
            return json_data
        
        return {"Data":"None"}
        # https://earnbigrwds.com/default.aspx?Flow=E5A922B4-A9F1-37AA-AD61-831BEB2F3512C71E33F6&subaff1=11725869122&subaff2=92372&subaff3=204413&subaff4=credits&email=jj8322289@gmail.com&phone=6467323660&reward=cash2xsummer&EntranceVID=mSmIngqL%7ClIIt-hPMAb7UA2&firstname=jack&lastname=john&dobday=5&dobmonth=3&dobyear=1999&gender=male&zippost=99141&state=WA&dom=1&affsecid=11725869122&subaff5=smax


class AirIndia(DataModule):
    def __init__(self):
        name        = 'AirIndia'
        base_url    = 'https://nps.airindia.in/'
        super().__init__(name, base_url)
    
    def retrieve_data(self, url):
        # Get additional data
        data = {}
        resp = requests.get(url, allow_redirects=False, verify=False)
        redirect_url = resp.headers['Location']
        if redirect_url:
            params = redirect_url.split('?')[1]
            for param in params.split('&'):
                key = param.split('=')[0]
                val = param.split('=')[1]
                data[key] = val
        
            json_data = json.dumps(data,ensure_ascii=False)
            return json_data
        
        return {"Data":"None"}

        # https://airindia.qualtrics.com/jfe/form/SV_8ralENYIAZB5sGi?PNR=4UHOP6&ORG=DEL&DES=YVR&PFN=AARSHDEEP%20SINGH&PLN=DHILLON&PEmail=AARSHDHILLON@OUTLOOK.COM&PPhone=%20447487710863&FlightNumber=AI185&FlightDate=02%20Feb%2024&Class=Q