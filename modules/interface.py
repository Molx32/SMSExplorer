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
            try:
                AirIndia()
                Instagram()
                Earnrwds()
                # Ukrwds() -- Need to execute JS
                Moj()
                Superprof()
                Konto()
                SuitsMeCard()
            except Exception as e:
                print(e)
                raise e

class SecurityInterface:
    def controlerSmsSearch(input_search, input_data, input_interesting):
        sec = Security()
        a = sec.filter_sms_search_data(input_data)
        b = sec.filter_sms_search_interesting(input_interesting)
        c = sec.filter_sms_search_search(input_search)
        return all([a, b, c])

    def controlerInvestigationSearch(input_search, input_unique, input_unqualified):
        sec = Security()
        a = sec.filter_investigation_search_search(input_search)
        b = sec.filter_investigation_search_unique(input_unique)
        c = sec.filter_investigation_search_unqualified(input_unqualified)
        return all([a, b, c])

    def controlerInvestigationUpdate(input_is_interesting, input_domain, input_tags):
        sec = Security()
        a = sec.filter_investigation_update_is_interesting(input_is_interesting)
        b = sec.filter_investigation_update_domain(input_domain)
        c = sec.filter_investigation_update_tags(input_is_interesting, input_tags)
        return all([a, b, c])

    def controlerAutomationSearch(input_search, input_legal, input_automated):
        sec = Security()
        a = sec.filter_automation_search_search(input_search)
        b = sec.filter_automation_search_legal(input_legal)
        c = sec.filter_automation_search_automated(input_automated)
        return all([a, b, c])

    def controlerAutomationUpdate(input_domain, input_is_legal, input_is_automated):
        sec = Security()
        a = sec.filter_automation_update_domain(input_domain)
        b = sec.filter_automation_update_is_legal(input_is_legal)
        c = sec.filter_automation_update_is_automated(input_is_automated)
        return all([a, b, c])
    
    def controlerReassignBoolean(input):
        if input == 'YES':
            return True
        elif input == 'NO':
            return False
        elif input == 'ALL':
            return None
        else:
            return input
    
    def controlerReassignString(input):
        if input is None:
            return ''
        return input