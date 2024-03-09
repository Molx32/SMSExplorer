import requests
from requests_html import HTMLSession

session = HTMLSession()
r = session.get('https://ukrwds.com/wjwjhoss')
r.html.render()  # this call executes the js in the page

# Get additional data
# data = {}
# resp = requests.get("https://ukrwds.com/wjwjhoss", allow_redirects=False, verify=False)
# print(resp.text)
# redirect_url = resp.headers['Location']
# if redirect_url:
#     params = redirect_url.split('?')[1]
#     for param in params.split('&'):
#         key = param.split('=')[0]
#         val = param.split('=')[1]
#         data[key] = val

#     json_data = json.dumps(data,ensure_ascii=False)
#     print(json_data)
