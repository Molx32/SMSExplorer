# System
import string
import re
import json
import urllib.parse
from config.config import Config

class Security:
    def __init__(self):
        self.ALLOWED_CHARS_FREE_SEARCH      = string.ascii_letters + string.digits + ':/.-_'
        self.ALLOWED_CHARS_DOMAIN           = string.ascii_letters + string.digits + ' .-_:@'
        self.ALLOWED_CHARS_USERNAME         = string.ascii_letters + string.digits + '_-.'
        self.ALLOWED_CHARS_USERNAME_EMAIL   = string.ascii_letters + string.digits + '_-.'
        self.ALLOWED_CHARS_SENDER           = string.ascii_letters + string.digits + '+ '
        self.ALLOWED_CHARS_RECEIVER         = string.ascii_letters + string.digits + '+ '
        self.ALLOWED_CHARS_COUNTRY          = string.ascii_letters
        self.ALLOWED_CHARS_SOURCE           = string.ascii_letters
        self.ALLOWED_CHARS_TAGS             = string.ascii_uppercase + ',_'
        self.URL_PATTERN                    = "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"
    
    def _check_char(self, word, allowed_charset):
        for char in word:
            if char not in allowed_charset:
                return False
        return True
    
    def is_empty_or_not_set(self, input):
        if input is None:
            return True
        if input == '':
            return True
        return False

    def is_yes_no(self, input):
        if input in ['YES','NO']:
            return True
        return False

    def is_yes_no_all(self, input):
        if input in ['YES','NO','ALL']:
            return True
        return False
    
    def is_safe_domain(self, domain):
        return self._check_char(domain, self.ALLOWED_CHARS_DOMAIN)
    
    def is_safe_username(self, username):
        return self._check_char(username, self.ALLOWED_CHARS_USERNAME)

    def is_safe_email(self, email):
        if email.count('@') == 1:
            username    = email.split('@')[0]
            domain      = email.split('@')[1]
            
            domain      = self._check_char(domain, self.ALLOWED_CHARS_DOMAIN)
            username    = self._check_char(username, self.ALLOWED_CHARS_USERNAME_EMAIL)

            return domain and username
            
        return False
    
    def is_safe_sender(self, sender):
        return self._check_char(sender, self.ALLOWED_CHARS_SENDER)
    
    def is_safe_receiver(self, receiver):
        return self._check_char(receiver, self.ALLOWED_CHARS_SENDER)
    
    def is_safe_country(self, country):
        return self._check_char(country, self.ALLOWED_CHARS_COUNTRY)

    def is_safe_source(self, source):
        return self._check_char(source, self.ALLOWED_CHARS_SOURCE)
    
    def is_safe_url(self, url):
        return re.findall(self.URL_PATTERN, url)
        
    def is_safe_json(self, data):
        try:
            json.loads(data)
            return True
        except:
            return False
    
    def is_integer(self, i):
        try:
            int(i)
            return True
        except:
            return False

    def is_multiple_of(self, mod,i):
        return (i % mod) == 0

    # ------------------------------------------------------------ #
    # -                      SANITIZERS                          - #
    # ------------------------------------------------------------ #
    def sanitize_url_remove_end_dot(self, url):
        if url[-1] == '.':
            return url[:len(url)-1]
        return url

    def sanitize_empty_if_null(self, var):
        return var if var else ""
    
    def sanitize_special_char(self, var):
        var = urllib.parse.quote_plus(var)
        var = var.replace('&','%26')
        return var
    
    def sanitize_bool_default_false(self, var):
        return str(var) or "False"
    
        

    # ------------------------------------------------------------ #
    # -                      SMS ENDPOINT                        - #
    # ------------------------------------------------------------ #
    def filter_sms_search_data(self, input_data):
        if input_data is None:
            return True
        if input_data == '':
            return True
        if input_data not in Config.SEARCH_FILTERS_DATA:
            return False
        return True

    def filter_sms_search_interesting(self, input_interesting):
        if input_interesting is None:
            return True
        if input_interesting == '':
            return True
        if input_interesting not in Config.SEARCH_FILTERS_INTERESTING:
            return False
        return True

    def filter_sms_search_search(self, input_search):
        if input_search is None:
            return True
        if input_search == '':
            return True
        
        # Check each char
        for char in input_search:
            if char not in self.ALLOWED_CHARS_FREE_SEARCH:
                return False

        return True


    # ---------------------------------------------------------------- #
    # -                      TARGETS ENDPOINT                        - #
    # ---------------------------------------------------------------- #
    def filter_target_search_search(self, input_search):
        if input_search is None:
            return True

        for char in input_search:
            if char not in self.ALLOWED_CHARS_FREE_SEARCH:
                return False
        
        return True


    # ---------------------------------------------------------------- #
    # -                         CATEGORIZE                           - #
    # ---------------------------------------------------------------- #
    def filter_categorize_search_search(self, input_search):
        if input_search is None:
            return True

        if input_search == '':
            return True

        for char in input_search:
            if char not in self.ALLOWED_CHARS_FREE_SEARCH:
                return False

        return True

    def filter_categorize_search_unqualified(self, input_unqualified):
        if input_unqualified is None:
            return True

        if input_unqualified == '':
            return True

        if input_unqualified not in ['YES','NO']:
            return False

        return True

    def filter_categorize_update_is_interesting(self, input_is_interesting):
        if input_is_interesting not in ['YES','NO']:
            return False
        return True

    def filter_categorize_update_domain(self, input_domain):
        return self.is_safe_domain(input_domain)

    def filter_categorize_update_tags(self, input_is_interesting, input_tags):
        if input_tags == '':
            return True

        # Check what 'input_tags' contains
        for char in input_tags:
            if char not in self.ALLOWED_CHARS_TAGS:
                return False

        # Filter tags based on 'is_interesting'
        if input_is_interesting == 'YES':
            if not set(input_tags.split(',')) <= set(Config.LIST_METADATA_INTERESTING_YES):
                return False
        if input_is_interesting == 'NO':
            if not set(input_tags.split(',')) <= set(Config.LIST_METADATA_INTERESTING_NO):
                return False
        return True


    # ------------------------------------------------------------- #
    # -                       AUTOMATION                          - #
    # ------------------------------------------------------------- #
    def filter_automation_search_search(self, input_search):
        if self.is_empty_or_not_set(input_search):
            return True

        for char in input_search:
            if char not in self.ALLOWED_CHARS_FREE_SEARCH:
                return False

        return True

    def filter_automation_search_legal(self, input_legal):
        if self.is_empty_or_not_set(input_legal):
            return True
        if self.is_yes_no_all(input_legal):
            return True
        return False

    def filter_automation_search_automated(self, input_automated):
        if self.is_empty_or_not_set(input_automated):
            return True
        if self.is_yes_no_all(input_automated):
            return True
        return False

    def filter_automation_update_domain(self, input_domain):
        return self.is_safe_domain(input_domain)
    
    def filter_automation_update_is_legal(self, input_legal):
        if self.is_empty_or_not_set(input_legal):
            return True
        if self.is_yes_no(input_legal):
            return True
        return False

    def filter_automation_update_is_automated(self, input_is_automated):
        if self.is_empty_or_not_set(input_is_automated):
            return True
        if self.is_yes_no(input_is_automated):
            return True
        return False

    # ------------------------------------------------------------- #
    # -                       AUDIT LOGS                          - #
    # ------------------------------------------------------------- #
    def filter_auditlogs_search(self, input_search):
        if self.is_empty_or_not_set(input_search):
            return True

        for char in input_search:
            if char not in self.ALLOWED_CHARS_FREE_SEARCH:
                return False

        return True

    def filter_auditlogs_start(self, input_start):
        if self.is_empty_or_not_set(input_start):
            return True

        if self.is_integer(input_start):
            if self.is_multiple_of(50,int(input_start)):
                return True
        return False

    def filter_auditlogs_offset(self, input_offset):
        if self.is_empty_or_not_set(input_offset):
            return True

        if self.is_integer(input_offset):
            if self.is_multiple_of(50,int(input_offset)):
                return True
        return False
