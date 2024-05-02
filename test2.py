import requests
import re

phone_regex = " \+[0-9]+ "
pin_regex = "PIN: [0-9]+\."
text = "Willkommen bei meinSiggi! Telefonnummer: +491789260811 - PIN: 239111. Einloggen unter https://www.nextbike.de/bielefeld/"

data = {}
data['login_page']  = 'https://www.nextbike.de/en/account/login'
data['login']       = re.search(phone_regex, text).group(0).replace(' ','')
data['password']    = re.search(pin_regex, text).group(0).replace('PIN: ','').replace('.','')