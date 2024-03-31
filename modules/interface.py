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
    def controlerSmsSearch(input_data, input_interesting, input_search):
        print("input_data" + str(input_data))
        print("input_interesting" + str(input_interesting))
        print("input_search" + str(input_search))
        sec = Security()
        a = sec.filter_sms_search_data(input_data)
        b = sec.filter_sms_search_interesting(input_interesting)
        c = sec.filter_sms_search_search(input_search)
        return all([a, b, c])

    def controlerTargetSearch(input_search):
        sec = Security()
        a = sec.filter_target_search_search(input_search)
        return all([a])

    def controlerInvestigationSearch(input_search, input_unique, input_unqualified):
        print("input_search" + str(input_search))
        print("input_unique" + str(input_unique))
        print("input_unqualified" + str(input_unqualified))
        sec = Security()
        a = sec.filter_investigation_search_search(input_search)
        b = sec.filter_investigation_search_unique(input_unique)
        c = sec.filter_investigation_search_unqualified(input_unqualified)
        return all([a, b, c])

    def controlerTargetUpdateInteresting(input_is_interesting, input_domain, input_tags):
        print("input_is_interesting" + str(input_is_interesting))
        print("input_domain" + str(input_domain))
        print("input_tags" + str(input_tags))
        sec = Security()
        a = sec.filter_investigation_update_is_interesting(input_is_interesting)
        b = sec.filter_investigation_update_domain(input_domain)
        c = sec.filter_investigation_update_tags(input_is_interesting, input_tags)
        return all([a, b, c])

    def controlerTargetUpdateAutomation(input_domain, input_is_legal, input_is_automated):
        return True