# System
import string
from config.config import Config

class Security:
    def __init__(self):
        self.FREE_SEARCH_ALLOWED_CHARS = ':/.-_' + string.ascii_letters + string.digits
        self.TAGS_ALLOWED_CHARS = ',_' + string.ascii_uppercase
        

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
            if char not in self.FREE_SEARCH_ALLOWED_CHARS:
                return False

        return True


    # ---------------------------------------------------------------- #
    # -                      TARGETS ENDPOINT                        - #
    # ---------------------------------------------------------------- #
    def filter_target_search_search(self, input_search):
        if input_search is None:
            return True

        for char in input_search:
            if char not in self.FREE_SEARCH_ALLOWED_CHARS:
                return False
        
        return True


    # ---------------------------------------------------------------- #
    # -                       INVESTIGATION                          - #
    # ---------------------------------------------------------------- #
    def filter_investigation_search_search(self, input_search):
        if input_search is None:
            return True

        if input_search == '':
            return True

        for char in input_search:
            if char not in self.FREE_SEARCH_ALLOWED_CHARS:
                return False

        return True

    def filter_investigation_search_unique(self, input_unique):
        if input_unique is None:
            return True
        
        if input_unique == '':
            return True

        if input_unique not in ['YES','NO']:
            return False

        return True

    def filter_investigation_search_unqualified(self, input_unqualified):
        if input_unqualified is None:
            return True

        if input_unqualified == '':
            return True

        if input_unqualified not in ['YES','NO']:
            return False

        return True

    def filter_investigation_update_is_interesting(self, input_is_interesting):
        if input_is_interesting not in ['YES','NO']:
            return False
        return True

    def filter_investigation_update_domain(self, input_domain):
        if input_domain == '' or not input_domain:
            return False
        return True

    def filter_investigation_update_tags(self, input_is_interesting, input_tags):
        if input_tags == '':
            print("first")
            return True

        # Check what 'input_tags' contains
        for char in input_tags:
            if char not in self.TAGS_ALLOWED_CHARS:
                print("second")
                return False

        # Filter tags based on 'is_interesting'
        if input_is_interesting == 'YES':
            print("yes")
            if not set(input_tags.split(',')) <= set(Config.LIST_METADATA_INTERESTING_YES):
                print("no subset")
                return False
        if input_is_interesting == 'NO':
            print("yes")
            if not set(input_tags.split(',')) <= set(Config.LIST_METADATA_INTERESTING_NO):
                print("no subset")
                return False
        print("last")
        return True
