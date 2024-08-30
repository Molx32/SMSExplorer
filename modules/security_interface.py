from modules.security.security import Security

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



############################## CONTROLER ################################
# Database object controlers and sanitizers                             #
#########################################################################
    def controlerObjectEmail(email):
        sec = Security()
        return sec.is_safe_email(email)

    def controlerObjectUsername(username):
        sec = Security()
        return sec.is_safe_username(username)
    
    def controlerObjectSender(sender):
        sec = Security()
        return sec.is_safe_sender(sender)
    
    def controlerObjectReceiver(receiver):
        sec = Security()
        return sec.is_safe_receiver(receiver)

    def controlerObjectMessage(message):
        # Since messages can contain any chars, do not control, but filter!
        return True
        
    def controlerObjectDate(date):
        # Return true because Python-validated
        return True

    def controlerObjectCountry(country):
        sec = Security()
        return sec.is_safe_country(country)
    
    def controlerObjectUrl(url):
        sec = Security()
        return sec.is_safe_url(url)

    def controlerObjectDomain(domain):
        sec = Security()
        return sec.is_safe_domain(domain)

    def controlerObjectSource(source):
        sec = Security()
        return sec.is_safe_source(source)

    def controlerObjectData(data):
        sec = Security()
        return sec.is_safe_json(data)
    



    def sanitizerObjectSender(sender):
        sec = Security()
        return sec.sanitize_special_char(sender)
    
    def sanitizerObjectReceiver(receiver):
        sec = Security()
        return sec.sanitize_special_char(receiver)
    
    def sanitizerObjectMessage(message):
        sec = Security()
        return sec.sanitize_special_char(message)
    
    def sanitizerObjectDate(date):
        sec = Security()
        return sec.sanitize_empty_if_null(date)
    
    def sanitizerObjectCountry(country):
        sec = Security()
        return sec.sanitize_empty_if_null(country)

    def sanitizerObjectUrl(url):
        sec = Security()
        ret = url
        ret = sec.sanitize_empty_if_null(ret)
        ret = sec.sanitize_url_remove_end_dot(ret)
        return ret

    def sanitizerObjectDomain(domain):
        sec = Security()
        return sec.sanitize_url_remove_end_dot(domain)
    
    def sanitizerObjectSource(source):
        sec = Security()
        return sec.sanitize_url_remove_end_dot(source)
    
    def sanitizerObjectDataHandled(data_handled):
        sec = Security()
        return sec.sanitize_bool_default_false(data_handled)

    def sanitizerObjectEmail(email):
        return email
    
    def sanitizerObjectUsername(username):
        return username