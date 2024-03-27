import requests
from bs4 import BeautifulSoup



headers = {
            'User-Agent':'toto'
        }
base = "https://receive-sms-free.cc/"
urls = ["https://receive-sms-free.cc/regions/", "https://receive-sms-free.cc/regions/2.html", "https://receive-sms-free.cc/regions/3.html"]

countries = []
for url in urls:
    r = requests.get(url, headers=headers, allow_redirects=True)
    soup = BeautifulSoup(r.text, features="lxml")
    for a in soup.find_all('a', 'link_btn trans'):
        country = base + a['href']
        countries.append(country)

nb = 0
for country in countries:
    for i in range(1,10):
        if i == 1:
            url = country
        else:
            url = country + str(i) + '.html'


        r = requests.get(url, headers=headers, allow_redirects=True)
        soup = BeautifulSoup(r.text, features="lxml")
        for span in soup.find_all('span'):
            if span is not None:
                if '+' in span.text:
                    number = span.text.replace('<span>','').replace('</span>','') + '\n'
                    with open('receive-sms-free.cc.csv', 'a') as f:
                        f.write(number)
