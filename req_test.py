import grequests
import requests
import time
import json
from bs4 import BeautifulSoup
import re

def http_get(url, allow_redirects=True):
    headers = {
        'User-Agent':'toto'
    }
    r = requests.get(url, headers=headers, allow_redirects=allow_redirects)
    return r

# r = http_get('https://mytempsms.com/receive-sms-online/france-phone-number-4589532415.html')
# urls = [
#     'https://mytempsms.com/receive-sms-online/france-phone-number-4589532415.html',
#     'https://mytempsms.com/receive-sms-online/france-phone-number-4589532415.html'
# ]
# results = grequests.map((grequests.get(u, headers={'User-Agent':'toto'}) for u in urls), size=10)
# for r in results:
#     print(r.status_code)

url     = 'https://receive-smss.com/sms/33780739376/'
print(url.split('/')[2])