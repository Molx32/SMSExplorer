import requests
from bs4 import BeautifulSoup



headers = {
            'User-Agent':'toto'
        }
base = "https://receive-smss.live"

r = requests.get(base, headers=headers, allow_redirects=True)
print(r.text)
soup = BeautifulSoup(r.text, features="lxml")
for h4 in soup.find_all('h4'):
    print(h4.text)