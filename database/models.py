import sys
import re

# Parse URLs
# import validator
# from urllib.parse import urlparse

sys.path.extend(['../'])

import urllib.parse
from config.config import Connections


class SMS:
    def __init__(self, sender, receiver, msg, receive_date, country):
        self.sender         = sender
        self.receiver       = receiver
        self.msg            = msg
        self.receive_date   = receive_date
        self.country        = country
        self.url            = ''
        self.domain         = ''
        self.source         = ""
        self.data_handled   = False

        # Parse receiver
        self.receiver = self.receiver.replace("%2F",'')
        self.receiver = self.receiver.replace("/",'')
        self.receiver = self.receiver.replace("sms",'')
        
        # Extract URL and domain
        url_match   = self._parseUrl()
        dom_match   = self._parseDomain()
        if url_match:
            self._sanitizeUrl(url_match)
            self.domain = self.url.split('/')[2]
    
    # Meta handling of attributes and their values
    def getAttributes(self):
        return ", ".join(list(self.__dict__.keys()))
    
    def getValues(self):
        return "'" + "', '".join(list(self.__dict__.values()))  + "'"

    def getValuesForDatabase(self):
        try:
            text = "'" 
            text = text + urllib.parse.quote_plus(self.sender) + "', '"
            text = text + urllib.parse.quote_plus(self.receiver) + "', '"
            text = text + urllib.parse.quote_plus(self.msg) + "', '"
            text = text + (self.receive_date or "") +  "', '"
            text = text + (self.country or "") + "', '"
            text = text + (self.url or "") + "', '"
            text = text + (self.domain or "") + "', '"
            text = text + (self.source or "") + "', '"
            text = text + (str(self.data_handled) or "False")
            text = text + "'"
            text.replace('&', '%26')
            return text
        except Exception as error:
            raise Exception("Message content unsafe, don't add to database." + str(self))
    
    def getAttributeValue(self, attribute):
        return self.__dict__['attribute']

    def setAttribute(self, attribute, value):
        setattr(self, attribute, value)
    
    def setAttributes(self, dict):
        for k, v in dict.items():
            setattr(self, k, v)

    # Methods
    def _parseUrl(self):
        # # Analyze each word
        # for word in self.msg.split(" "):
        #     try:
        #         if validators.url(word):
        #             url = word
        #     except:
        #         continue
        # return url
        url_pattern = "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"
        return re.findall(url_pattern, self.msg)

    def _sanitizeUrl(self, url_match):
        self.url = url_match[0]
        # Remove dot at the end
        if self.url[-1] == '.':
            self.url = self.url[:len(self.url)-1]
    
    def _parseDomain(self):
        dom_pattern = "^((?!-)[A-Za-z0-9-]" + "{1,63}(?<!-)\\.)" +"+[A-Za-z]{2,6}"
        return re.findall(dom_pattern, self.msg)

    def _parse_msg(self):
        self.msg = self.msg.replace('p***word', 'password')
        self.msg = self.msg.replace('do***ent', 'document')
        self.msg = self.msg.replace('iden***y', 'identity')
        self.msg = self.msg.replace('***igned', 'assigned')

    def __str__(self):
        keys = ", ".join(list(self.__dict__.keys()))
        values = ", ".join(list(self.__dict__.values()))
        return values
        return keys + '\n' + values

    def __eq__(self, obj):
        return isinstance(obj, SMS) and obj.receiver == self.receiver and obj.sender == self.sender and obj.msg == self.msg