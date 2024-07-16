import requests
import uuid


headers = {
    'User-Agent':'classic'
}

# rs      = (grequests.get(url) for url in urls_fr)
# results = grequests.map(rs)
# for r in results:
#     if r:
#         print(str(r.status_code) + ' - ' + r.request.url)

url     = "https://receive-smss.com/"
params  = {"appId":"1:780034453512:web:7b7ec6e76f6f04049ca1bd", "appInstanceId":"required_but_unused_value"}
headers = {"User-Agent":str(uuid.uuid4())}
r = requests.get(url, params=params, headers=headers)
print(r)
print(r.status_code)
print(r.text)