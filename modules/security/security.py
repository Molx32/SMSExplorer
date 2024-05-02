# System
import string
from config.config import Config

class Security:
    def __init__(self):
        self.ALLOWED_CHARS_FREE_SEARCH = ':/.-_' + string.ascii_letters + string.digits
        self.ALLOWED_CHARS_TAGS = ',_' + string.ascii_uppercase
        self.ALLOWED_CHARS_DOMAIN = ' .-_:@' + string.ascii_letters + string.digits
    
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
    
    def is_domain_safe(self, domain):
        for char in domain:
            if char not in self.ALLOWED_CHARS_DOMAIN:
                return False
        return True


        

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
        return self.is_domain_safe(input_domain)

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
        return self.is_domain_safe(input_domain)
    
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