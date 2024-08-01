import sys
import rq
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
                # Instagram()
                Earnrwds()
                # Ukrwds() -- Need to execute JS
                Moj()
                Superprof()
                Konto()
                SuitsMeCard()
                Booksy()
                Lilly()
                Rwdsuk()
                StickerMule()
            except Exception as e:
                raise e

class SecurityInterface:
    def controlerSmsSearch(input_search, input_data, input_interesting):
        sec = Security()
        a = sec.filter_sms_search_data(input_data)
        b = sec.filter_sms_search_interesting(input_interesting)
        c = sec.filter_sms_search_search(input_search)
        return all([a, b, c])

    def controlerCategorizeSearch(input_search, input_unqualified):
        sec = Security()
        a = sec.filter_categorize_search_search(input_search)
        b = sec.filter_categorize_search_unqualified(input_unqualified)
        return all([a, b])

    def controlerCategorizeUpdate(input_is_interesting, input_domain, input_tags):
        sec = Security()
        a = sec.filter_categorize_update_is_interesting(input_is_interesting)
        b = sec.filter_categorize_update_domain(input_domain)
        c = sec.filter_categorize_update_tags(input_is_interesting, input_tags)
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
    
    def controlerReassignInteger(input):
        if input:
            return input
        return 0
    
    def controlerReassignString(input):
        if input is None:
            return ''
        return input

    def controlerAuditLogsSearch(input_search, input_start, input_offset):
        sec = Security()
        a = sec.filter_auditlogs_search(input_search)
        b = sec.filter_auditlogs_start(input_start)
        c = sec.filter_auditlogs_offset(input_offset)
        return all([a, b, c])

    def controlerReassignDbStartEnd(input_start, input_end):
        try:
            start       = max(int(input_start), 0)
            end         = max(int(input_end), 50)
        except Exception:
            start       = 0
            end         = 50
        return start, end