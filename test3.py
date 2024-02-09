# https://nps.airindia.in/w1ZoZvh4

# import requests

# url = 'https://nps.airindia.in/mCOdZVTh'
# rep = requests.get(url, allow_redirects=False, verify=False)
# redirect_url = rep.headers['Location']
# params = redirect_url.split('?')[1]
# for param in params.split('&'):
#     key = param.split('=')[0]
#     val = param.split('=')[1]
#     print(key + ' - ' + val)

import json
 
# Create a dictionary
sms_id = 1
json_data = "test"
s = """ INSERT INTO DATA(SMS_DATA,SMS_ID) VALUES('{}', {}); """.format(json_data, sms_id)
print(s)

smss = (13, 'https://w-mt.co/g/9GbFdJ')
