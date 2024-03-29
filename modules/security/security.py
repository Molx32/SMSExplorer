# System
import string
from config.config import Config

class Security:
    def __init__(self):
        self.search_allowed_chars = ':/.-_' + string.ascii_letters + string.digits

    def filter_sms_search_data(self, input_data):
        if input_data is None:
            return True
        if input_data not in Config.SEARCH_FILTERS_DATA:
            return False
        return True

    def filter_sms_search_interesting(self, input_interesting):
        if input_interesting is None:
            return True
        if input_interesting not in Config.SEARCH_FILTERS_INTERESTING:
            return False
        return True

    def filter_sms_search_search(self, input_search):
        if input_search is None:
            return True
        
        # Check each char
        for char in input_search:
            if char not in self.search_allowed_chars:
                return False

        return True
            