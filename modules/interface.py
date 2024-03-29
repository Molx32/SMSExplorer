import sys
from modules.target.target_receive_smss import ReceiveSMSS
from modules.target.target_mytempsms import MyTempSMS
from modules.security.security import Security

from modules.data.data__module import *

sys.path.extend(['../'])

class TargetInterface:
    
    def create_instance_receivesmss():
        return ReceiveSMSS()
    
    def create_instance_mytempsms():
        return MyTempSMS()

class DataInterface:

    def create_data_fetcher():
        while 1:
            AirIndia()
            Instagram()
            Earnrwds()
            # Ukrwds() -- Need to execute JS
            Moj()
            Superprof()
            Konto()
            SuitsMeCard()

class SecurityInterface:
    def controlerSearch(input_data, input_interesting, input_search):
        sec = Security()
        a = sec.filter_sms_search_data(input_data)
        b = sec.filter_sms_search_interesting(input_interesting)
        c = sec.filter_sms_search_search(input_search)
        return all([a, b, c])