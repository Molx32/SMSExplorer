import requests
from html.parser import HTMLParser
import pandas as pd
import re

class MyHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.in_table = False
        self.in_row = False
        self.in_col = False

        self.row_count = 0
        self.row_str = ''

        self.data = False

    def handle_starttag(self, tag, attrs):
        if tag == 'tbody':
            self.in_table = True
        
        elif tag == 'tr' and self.in_table:
            self.in_row = True

        elif tag == 'td' and self.in_table and self.in_row:
            self.in_col = True
            self.data = True

            
    def handle_endtag(self, tag):
        if tag == 'tbody' and self.in_table:
            self.in_table = False
        
        elif tag == 'tr' and self.in_table and self.in_row:
            self.in_row = False
            print("FINNNNNNNNNNNNNNNNNNNNN")

        elif tag == 'td' and self.in_table and self.in_row and self.in_col:
            self.in_col = False
            self.data = False
        else:
            pass

    def handle_data(self, data):
        if self.data:
            print(data)
            print("DATAAAAAAAAAAAAAAAAAAAA")

# parser = MyHTMLParser()

url = "https://receive-smss.com/sms/33780739376/"
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 OPR/101.0.0.0'
}
r = requests.get(url, headers=headers)
# parser.feed(r.text)




# url = r'https://receive-smss.com/sms/33780739376/'
tables = pd.read_html(r.text) # Returns list of all tables on page
sp500_table = tables[0]
print(sp500_table)