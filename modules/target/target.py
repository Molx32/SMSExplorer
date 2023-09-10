from html.parser import HTMLParser
import requests

class Target:

    def __init__(self):
        self.base_url = ""
        self.phone_urls = []
        self.parser_phone   = None
        self.parser_sms     = None

        

    def fetch_phones(self):
        pass

    def fetch_smss(self):
        for phone in self.phone_urls:
            pass
    
    def fetch_sms(self):
        pass

    def send_request_get(self, url):
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 OPR/101.0.0.0'
        }
        return requests.get(url, headers=headers)
