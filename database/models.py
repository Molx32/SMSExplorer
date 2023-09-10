import sys
sys.path.extend(['../'])

from config.config import Connections
import psycopg2


class SMS:
    def __init__(self):
        self.receive_date   = None
        self.sender         = None
        self.receiver       = None
        self.msg            = None
        
    def getAttributes(self):
        return ", ".join(list(self.__dict__.keys()))
    
    def getValues(self):
        return "'" + "', '".join(list(self.__dict__.values()))  + "'"
    
    def getAttributeValue(self, attribute):
        return self.__dict__['attribute']

    def setAttribute(self, attribute, value):
        setattr(self, attribute, value)
    
    def setAttributes(self, dict):
        for k, v in dict.items():
            setattr(self, k, v)
            print(str(k) + ',' + str(v))

    def __str__(self):
        keys = ", ".join(list(self.__dict__.keys()))
        values = ", ".join(list(self.__dict__.values()))
        return keys + '\n' + values