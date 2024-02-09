import requests
from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
# pip install selenium
# pip install webdriver_manager

url = 'https://receive-smss.com'
browser = Chrome()
browser.get(url)



# Phones
phone_urls = []
class_a = "number-boxes1-item-button number-boxess1-item-button button blue stroke rounded tssb"
soup = BeautifulSoup(browser.page_source, features="lxml")
for a in soup.find_all('a'):
    try:
        if class_a in " ".join(a.get('class')):
            sender = a.get('href')
            phone_urls.append(sender)
    except Exception as e:
        # print(e)
        pass

print(len(phone_urls))


class_sender = "col-md-3 sender"
class_msg    = "col-md-6 msg"
class_time   = "col-md-3 time"
for phone_url in phone_urls:
    # Analyse and get SMSs
    # Parse with BeautifulSoup
    print(url+phone_url)
    browser.get(url+phone_url)
    soup2 = BeautifulSoup(browser.page_source, features="lxml")
    # Initialize next SMS
    
    # Iterate over all 'div'. Once we retrieved each attribute,
    # we can build a SMS object and reset temporary attributes
    # to None.
    for div in soup2.find_all('div'):
        try:
            if class_sender in " ".join(div.get('class')):
                sender = div.get_text().replace("Sender",'')
                print(sender)
            if class_msg in " ".join(div.get('class')):
                msg = div.get_text().replace("Message",'').replace('\n','')
                print(msg)
            if class_time in " ".join(div.get('class')):
                time = div.get_text().replace("Time",'')
                print(time)
        except:
            pass
    