import sys
import re
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
        self.instagram_acc  = None
        self.source         = ""
        self.url            = 'NOT FOUND'
        self.domain         = 'NOT FOUND'

        # Extract URL and domain
        url_pattern = url_pattern = "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"
        dom_pattern = "^((?!-)[A-Za-z0-9-]" + "{1,63}(?<!-)\\.)" +"+[A-Za-z]{2,6}"
        url_match   = re.findall(url_pattern, self.msg)
        dom_match   = re.findall(dom_pattern, self.msg)
        if url_match:
            self.url = url_match[0]
        if dom_match:
            self.domain = dom_match[0]
    
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
            text = text + (self.instagram_acc or "") + "', '"
            text = text + (self.url or "") + "', '"
            text = text + (self.domain or "") + "', '"
            text = text + (self.source or "")
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
    def add_instagram_account(self, instagram_acc):
        self.instagram_acc = instagram_acc

    def __str__(self):
        keys = ", ".join(list(self.__dict__.keys()))
        values = ", ".join(list(self.__dict__.values()))
        return values
        return keys + '\n' + values

    def __eq__(self, obj):
        return isinstance(obj, SMS) and obj.receiver == self.receiver and obj.sender == self.sender and obj.msg == self.msg