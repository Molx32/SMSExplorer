import sys
import re
from datetime import datetime


sys.path.extend(['../'])

import urllib.parse
from config.config import Connections
from database.database import DatabaseInterface
from interfaces.security_interface import SecurityInterface
from flask_login import UserMixin


class Model:
    def __init__(self, pk = None):
        self.pk = pk
        self.attributes = {}

    def getAttributes(self):
        return ", ".join(list(self.attributes.keys()))
    
    def getValues(self):
        return "'" + "', '".join(str(e) for e in list(self.attributes.values()))  + "'"
    
    def insert(self):
        pass

class User(UserMixin):
    id          = None
    username    = None
    password    = None
    role        = None

class Data(Model):
    def __init__(self, pk, username, email, raw, sms_id):
        super().__init__(pk)
        
        # Database mapping
        self.attributes['data_raw']         = username
        self.attributes['data_username']    = email
        self.attributes['data_email']       = raw
        self.attributes['sms_id']           = sms_id
    
    # Sanitize data to be inserted
    def security_controler(self):
        self.attributes['email']     = SecurityInterface.controlerObjectEmail       (self.attributes['email'])
        self.attributes['username']  = SecurityInterface.controlerObjectUsername    (self.attributes['username'])

    def security_sanitizer(self):
        self.attributes['email']     = SecurityInterface.sanitizerObjectEmail        (self.attributes['email'])
        self.attributes['username']  = SecurityInterface.sanitizerObjectUsername     (self.attributes['username'])

    # Insert into database
    def insert(self):
        self.security_controler()
        self.security_sanitizer()
        DatabaseInterface.data_insert(self)

class SMS(Model):
    def __init__(self, pk, sender, receiver, msg, receive_date, country):
        super().__init__(pk)

        # Parse input
        msg         = self.parse_msg(msg)
        receiver    = self.parse_receiver(receiver)
        url         = self.parse_url(msg)
        domain      = self.parse_domain(url)

        # Database mapping
        self.attributes['sender']         = sender
        self.attributes['receiver']       = receiver
        self.attributes['msg']            = msg
        self.attributes['receive_date']   = receive_date
        self.attributes['country']        = country
        self.attributes['url']            = url
        self.attributes['domain']         = domain
        self.attributes['source']         = ""
        self.attributes['data_handled']   = False

        self.security_sanitizer()


    # Control data to be inserted
    def security_controler(self):
        try:
            controler = True
            controler = controler and SecurityInterface.controlerObjectSender     (self.attributes['sender'])
            controler = controler and SecurityInterface.controlerObjectReceiver   (self.attributes['receiver'])
            controler = controler and SecurityInterface.controlerObjectMessage    (self.attributes['msg'])
            controler = controler and SecurityInterface.controlerObjectDate       (self.attributes['receive_date'])
            controler = controler and SecurityInterface.controlerObjectCountry    (self.attributes['country'])
            controler = controler and SecurityInterface.controlerObjectUrl        (self.attributes['url'])
            controler = controler and SecurityInterface.controlerObjectDomain     (self.attributes['domain'])
            controler = controler and SecurityInterface.controlerObjectSource     (self.attributes['source'])
            controler = controler and SecurityInterface.controlerObjectData       (self.attributes['data_handled'])
            return True
        except Exception as error:
            raise Exception("Security controler : Message content unsafe, don't add to database." + str(self)) from error

    # Control data to be inserted
    def security_sanitizer(self):
        try:
            self.attributes['sender']         = SecurityInterface.sanitizerObjectSender     (self.attributes['sender'])
            self.attributes['receiver']       = SecurityInterface.sanitizerObjectReceiver   (self.attributes['receiver'])
            self.attributes['msg']            = SecurityInterface.sanitizerObjectMessage    (self.attributes['msg'])
            self.attributes['receive_date']   = SecurityInterface.sanitizerObjectDate       (self.attributes['receive_date'])
            self.attributes['country']        = SecurityInterface.sanitizerObjectCountry    (self.attributes['country'])
            self.attributes['url']            = SecurityInterface.sanitizerObjectUrl        (self.attributes['url'])
            self.attributes['domain']         = SecurityInterface.sanitizerObjectDomain     (self.attributes['domain'])
            self.attributes['source']         = SecurityInterface.sanitizerObjectSource     (self.attributes['source'])
            self.attributes['data_handled']   = SecurityInterface.sanitizerObjectDataHandled(self.attributes['data_handled'])
        except Exception as error:
            raise Exception("Security sanitizer : Message content unsafe, don't add to database." + str(self)) from error

    # Insert into database
    def insert(self):
        # self.security_controler()
        # self.security_sanitizer()
        DatabaseInterface.sms_insert(self)

    # Methods
    def parse_url(self, msg):
        url_pattern = "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"
        match = re.findall(url_pattern, msg)
        if match:
            url = match[0]
            if url[-1] == '.':
                return url[:len(url)-1]
            return url
        return None
    
    def parse_domain(self, url):
        if url:
            return url.split('/')[2]
        return None
        dom_pattern = "^((?!-)[A-Za-z0-9-]" + "{1,63}(?<!-)\\.)" +"+[A-Za-z]{2,6}"
        match = re.findall(dom_pattern, msg)
        if match:
            return match[0]
        return None

    def parse_msg(self, msg):
        msg = msg.replace('p***word', 'password')
        msg = msg.replace('do***ent', 'document')
        msg = msg.replace('iden***y', 'identity')
        msg = msg.replace('***igned', 'assigned')
        return msg
    
    def parse_receiver(self, receiver):
        # Parse receiver
        receiver = receiver.replace("%2F",'')
        receiver = receiver.replace("/",'')
        receiver = receiver.replace("sms",'')
        return receiver

    def __str__(self):
        values = ", ".join(str(e) for e in list(self.attributes.values()))
        return values

    def __eq__(self, obj):
        return isinstance(obj, SMS) and obj.attributes['receiver'] == self.attributes['receiver'] and obj.attributes['sender'] == self.attributes['sender'] and obj.attributes['msg'] == self.attributes['msg']
    
class AuditLog(Model):
    def __init__(self, pk, resp):
        super().__init__(pk)
        
        self.attributes['http_req_date']        = self.format_date()
        self.attributes['http_verb']            = resp.request.method
        self.attributes['http_resp_code']       = str(resp.status_code) + " " + resp.reason
        self.attributes['http_resp_content']    = ""
        self.attributes['http_req']             = resp.url

        self.security_sanitizer()


    # Control data to be inserted
    def security_controler(self):
        try:
            controler = True
            return controler
        except Exception as error:
            raise Exception("Security controler : Message content unsafe, don't add to database." + str(self)) from error

    # Control data to be inserted
    def security_sanitizer(self):
        try:
            pass
        except Exception as error:
            raise Exception("Security sanitizer : Message content unsafe, don't add to database." + str(self)) from error

    # Insert into database
    def log(self):
        DatabaseInterface.log(self)

    def format_date(self):
        http_req_date       = datetime.now()
        http_req_date       = http_req_date.strftime("%m/%d/%Y %H:%M:%S")
        return http_req_date

    def __str__(self):
        values = ", ".join(str(e) for e in list(self.attributes.values()))
        return values

    def __eq__(self, obj):
        return isinstance(obj, SMS) and obj.attributes['receiver'] == self.attributes['receiver'] and obj.attributes['sender'] == self.attributes['sender'] and obj.attributes['msg'] == self.attributes['msg']