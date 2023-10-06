import sys
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
    
    # Meta handling of attributes and their values
    def getAttributes(self):
        return ", ".join(list(self.__dict__.keys()))
    
    def getValues(self):
        return "'" + "', '".join(list(self.__dict__.values()))  + "'"

    def getValuesForDatabase(self):
        try:
            text = "'" + urllib.parse.quote_plus(self.sender) + "', '" + urllib.parse.quote_plus(self.receiver) + "', '" + urllib.parse.quote_plus(self.msg) + "', '" + self.receive_date +  "', '" + self.country + "', '" + self.instagram_acc + "'"
        except Exception as error:
            raise Exception("Message content unsafe, don't add to database.")
        text.replace('&', '%26')
        return text
    
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