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
requests.packages.urllib3.disable_warnings()
import pandas as pd
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
                for sms in self.smss:
                    #DATA - Mock - run - 'Mock' object has no attribute 'data'
                    sms_id  = sms[0]
                    url     = sms[1]
                    msg     = sms[2]
                    data    = self.retrieve_data(url, msg)
                    if data:
                        self.populate_database(sms_id, data)

        except Exception as e:
            Logger.log('DATA - ' + self.name + ' - run - ' + str(e))

    def populate_database(self, sms_id, data):
        try:
            # Insert new SMSs into database
            DatabaseInterface.sms_insert_data(sms_id, data)
        except Exception as e:
            Logger.log('DATA - ' + self.name + ' - populate_database - ' + str(e))

    def retrieve_data(self, url, msg):
        return None

    def _retrieve_data_in_msg(self, msg):
        return None

    def _retrieve_data_redirect(self, url):
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


class Instagram(DataModule):
    def __init__(self):
        name        = 'Instagram'
        base_url    = 'https://ig.me/'

        self.current_url = ""

        super().__init__(name, base_url)

    
    def retrieve_data(self, url, msg):
        self.current_url = url
        self._parse_instagram_transform_url()
        return self._parse_instagram()
    
    def _parse_instagram_transform_url(self):
        # Remove dot at the end if exists
        last_char   = self.current_url[-1]
        l           = len(self.current_url)
        if last_char == '.':
            self.current_url = self.current_url[:l-1]

        source  = requests.get(self.current_url, allow_redirects=False)
        next_url = source.headers['Location']
        
        # Handle mobile shit
        if 'instagram://smslogin' in next_url:
            self.current_url = next_url
            self.current_url = self.current_url.replace('instagram://smslogin/', 'https://www.instagram.com/_n/web_smslogin')
            self.current_url = self.current_url.replace('utm_campaign=smslogin', 'utm_campaign=web_smslogin')
        
    def _parse_instagram(self):
        # Send request and parse it
        response = requests.get(self.current_url, allow_redirects=True)
        soup = BeautifulSoup(response.text, features="lxml")

        try:
            # Get SVG tag that contains 'Profile', then get its parent
            svgs = soup.find_all('svg', attrs={"aria-label" : "Profile", "class":"simple-nav__svgIcon"})
            a = svg.find_parent('a')
            acc = a['href'].replace('/','')
            return {"data":acc}
        except:
            return None

class Ukrwds(DataModule):
    def __init__(self):
        name        = 'Ukrwds'
        base_url    = 'https://ukrwds.com/'
        super().__init__(name, base_url)
    
    def retrieve_data(self, url, msg):
        return self._retrieve_data_redirect(url)
        # https://earnbigrwds.com/default.aspx?Flow=E5A922B4-A9F1-37AA-AD61-831BEB2F3512C71E33F6&subaff1=11725869122&subaff2=92372&subaff3=204413&subaff4=credits&email=jj8322289@gmail.com&phone=6467323660&reward=cash2xsummer&EntranceVID=mSmIngqL%7ClIIt-hPMAb7UA2&firstname=jack&lastname=john&dobday=5&dobmonth=3&dobyear=1999&gender=male&zippost=99141&state=WA&dom=1&affsecid=11725869122&subaff5=smax

class Earnrwds(DataModule):
    def __init__(self):
        name        = 'Earnrwds'
        base_url    = 'https://earnrwds.com/'
        super().__init__(name, base_url)
    
    def retrieve_data(self, url, msg):
        return self._retrieve_data_redirect(url)
        # https://earnbigrwds.com/default.aspx?Flow=E5A922B4-A9F1-37AA-AD61-831BEB2F3512C71E33F6&subaff1=11725869122&subaff2=92372&subaff3=204413&subaff4=credits&email=jj8322289@gmail.com&phone=6467323660&reward=cash2xsummer&EntranceVID=mSmIngqL%7ClIIt-hPMAb7UA2&firstname=jack&lastname=john&dobday=5&dobmonth=3&dobyear=1999&gender=male&zippost=99141&state=WA&dom=1&affsecid=11725869122&subaff5=smax

class AirIndia(DataModule):
    def __init__(self):
        name        = 'AirIndia'
        base_url    = 'https://nps.airindia.in/'
        super().__init__(name, base_url)
    
    def retrieve_data(self, url, msg):
        return self._retrieve_data_redirect(url)
        # https://airindia.qualtrics.com/jfe/form/SV_8ralENYIAZB5sGi?PNR=4UHOP6&ORG=DEL&DES=YVR&PFN=AARSHDEEP%20SINGH&PLN=DHILLON&PEmail=AARSHDHILLON@OUTLOOK.COM&PPhone=%20447487710863&FlightNumber=AI185&FlightDate=02%20Feb%2024&Class=Q

class Moj(DataModule):
    def __init__(self):
        name        = 'Moj'
        base_url    = 'https://force-us-app.moj.io/'
        super().__init__(name, base_url)
    
    def retrieve_data(self, url, msg):
        return self._retrieve_data_redirect(url)
        # https://force-us-app.moj.io/onboard?firstName=Driver&lastName=Man&phoneNumber=19172132492&email=driverman@moj.io&resetToken=a57f5bba-c059-4dce-9e91-9506b2a7fa64

class Superprof(DataModule):
    def __init__(self):
        name        = 'Superprof'
        base_url    = 'https://www.superprof.es/'
        super().__init__(name, base_url)

    def retrieve_data(self, url, msg):
        # Access app and get SESSION cookie
        response    = requests.get(url, allow_redirects=False, verify=False)
        cookies     = response.headers['Set-Cookie']
        cookie      = re.search(r'PHPSESSID=.*;', cookies).group(0)
        session_cookie_k    = cookie.split('=')[0]
        session_cookie_v    = cookie.split('=')[1]
        session_cookie      = {session_cookie_k:session_cookie_v}

        # Use SESSION cookie to get API Authorization token
        url = self.base_url + 'api/v3/authorize/'
        response    = requests.get(url, allow_redirects=False, verify=False, cookies=session_cookie)
        data        = response.json()
        token       = data['token_type'] + ' ' + data['access_token']
        headers     = {'Authorization': token}
        # Get data
        url = self.base_url + 'api/v3/me/'
        response    = requests.get(url, allow_redirects=False, verify=False, cookies=session_cookie, headers=headers)
        if response.json():
            return response.json()
        return {"Data":"None"}

class Konto(DataModule):
    def __init__(self):
        name        = 'Konto'
        base_url    = 'https://app.konto.com/'
        super().__init__(name, base_url)

    def retrieve_data(self, url, msg):
        return _retrieve_data_in_msg(msg)

    def _retrieve_data_in_msg(self, msg):
        return {"data":msg.split('sent you')[0]}

class SuitsMeCard(DataModule):
    def __init__(self):
        name        = 'SuitsMeCard'
        base_url    = 'https://suitsmecard.com/'
        super().__init__(name, base_url)

    def retrieve_data(self, url, msg):
        return _retrieve_data_in_msg(msg)

    def _retrieve_data_in_msg(self, msg):
        return {"data":msg.split('.')[0].replace('Hi ')}