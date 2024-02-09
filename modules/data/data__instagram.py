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
from data__module import DataModule

# Web
import requests
import pandas as pd
import requests
from bs4 import BeautifulSoup

class Instagram(DataModule):
    def __init__(self, delay):
        def __init__(self, delay):
        name        = 'Instagram'
        base_url    = 'https://ig.me/'
        super().__init__(name, base_url, delay)

    def retrieve_data(self, url):
        # Get additional data
        data = {}
        resp = requests.get(url, allow_redirects=False, verify=False)
        redirect_url = rep.headers['Location']
        params = redirect_url.split('?')[1]
        for param in params.split('&'):
            key = param.split('=')[0]
            val = param.split('=')[1]
            data[key] = val
        
        json_data = json.dumps(data,ensure_ascii=False)
        return json_data

        # https://airindia.qualtrics.com/jfe/form/SV_8ralENYIAZB5sGi?PNR=4UHOP6&ORG=DEL&DES=YVR&PFN=AARSHDEEP%20SINGH&PLN=DHILLON&PEmail=AARSHDHILLON@OUTLOOK.COM&PPhone=%20447487710863&FlightNumber=AI185&FlightDate=02%20Feb%2024&Class=Q

    def parse_instagram(self, sms):
        Logger.log('Browser - parse_instagram')
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
            Logger.log('EXCEPTION - PARSE INSTAGRAM CALL PATTERN - ' + str(e))