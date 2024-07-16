import requests
import re
from bs4 import BeautifulSoup

# https://ig.me/1TD3aNddCvdSto1
# https://instagram.com/accounts/password/reset/confirm/?uidb36=ugjz2wd&token=7dDIloqRVHoEAalwCaXVeO79LaeUdVmfx9anDxTvojpz2ChUSeBK6gfho18AJf4I:password_reset_sms&v=390.0.0.9.116&s=password_reset_sms&ndid=61778b7d13791Hf700e0c6dH6177901673a63H46&utm_medium=sms
# https://www.instagram.com/accounts/password/reset/confirm/?uidb36=ugjz2wd&token=7dDIloqRVHoEAalwCaXVeO79LaeUdVmfx9anDxTvojpz2ChUSeBK6gfho18AJf4I:password_reset_sms&v=390.0.0.9.116&s=password_reset_sms&ndid=61778b7d13791Hf700e0c6dH6177901673a63H46&utm_medium=sms
# https://www.instagram.com/api/v1/accounts/password/reset/confirmation_web/?source=password_reset_sms&token=7dDIloqRVHoEAalwCaXVeO79LaeUdVmfx9anDxTvojpz2ChUSeBK6gfho18AJf4I:password_reset_sms&uidb36=ugjz2wd


# ?uidb36=ugjz2wd&token=7dDIloqRVHoEAalwCaXVeO79LaeUdVmfx9anDxTvojpz2ChUSeBK6gfho18AJf4I:password_reset_sms&s=password_reset_sms&ndid=61778b7d13791Hf700e0c6dH6177901673a63H46&utm_medium=sms
# ?source=password_reset_sms&token=7dDIloqRVHoEAalwCaXVeO79LaeUdVmfx9anDxTvojpz2ChUSeBK6gfho18AJf4I:password_reset_sms&uidb36=ugjz2wd

urls = [
    # "https://ig.me/1TD3aNddCvdSto1",
    # "https://ig.me/1XhPlfLFHjpN1Xx",
    # "https://ig.me/1OwI8YocMFWZqPT",
    # "https://ig.me/1T4f9rpCwDaTTd9", --> Account disabled
    "https://ig.me/22nteweQuSP6pyv",
    "https://ig.me/1PNvhADWlxacYUA",
    "https://ig.me/2dCNU95xxdDbPWs",
    "https://ig.me/1Sby2Uh6pJaFlqQ",
    "https://ig.me/1Q7xjSIhHAI2wSn",
    "https://ig.me/1NYPVXWvuzuQ7Vs",
    "https://ig.me/1WLwM5EBNvbwAnU",
    "https://ig.me/1SSMWFZUwMuYkR9",
    "https://ig.me/2enqSZoCSIUVxUv",
    "https://ig.me/1IdbfD9oZWNsRNz",
    "https://ig.me/2cp6eATQBMnSAvr",
    "https://ig.me/1VPIEMhkJ9bEBR9",
    "https://ig.me/1QCjUMFxc5cb6uN",
    "https://ig.me/1IxUyVaxH7O2vYd",
    "https://ig.me/1NFh8xd0PnOs14U",
    "https://ig.me/1Mq9vL6s5fZbq2p",
    "https://ig.me/2dJnwEdBR2XvvVS",
    "https://ig.me/2dJnwEdBR2XvvVS",
    "https://ig.me/22CEUqP6TplrhGy",
    "https://ig.me/1Pw5ehBfutOdHkq",
    "https://ig.me/2isLOOJ76hKBREm",
    "https://ig.me/1ERpDU2dd7IbSje",
    "https://ig.me/1OTkliA5gtNuQDS",
    "https://ig.me/1He5aCWxirrx6ww",
    "https://ig.me/2mxiim8yaAyNUCv",
    "https://ig.me/1Q0rY98zcWHd5Vm",
    "https://ig.me/1F6bphiGAT60A8V",
    "https://ig.me/24JjH2ku63rOEbo",
    "https://ig.me/2QWPi1UuAtO54Up",
    "https://ig.me/1Trf0XhsbgbctRu",
    "https://ig.me/1XLNyXNN2v7ARMU",
    "https://ig.me/1Ql1F69aev0H9ET",
    "https://ig.me/bn6N23ZWUsjnq0"
]

for url in urls:
    source  = requests.get(url, allow_redirects=False)
    next_url = source.headers['Location']
    if not "www.instagram.com" in next_url:
        next_url = next_url.replace('instagram.com', 'www.instagram.com')

    # Case 1
    # https://instagram.com/accounts/password/reset/confirm
    # if "instagram.com/accounts/password/reset/confirm" in next_url:




    print("Req  1 : " + str(url))
    print("Resp 1 : " + str(source.status_code))
    print("Next URL :            " + str(next_url))

    # Handle mobile shit
    url = next_url
    if 'instagram://smslogin' in next_url:
        url = url.replace('instagram://smslogin/', 'https://www.instagram.com/_n/web_smslogin')
        url = url.replace('utm_campaign=smslogin', 'utm_campaign=web_smslogin')
    print("Next URL transformed: " + str(url))

    # Send request and parse it
    response = requests.get(url, allow_redirects=True)
    print("Req  2 : " + str(url))
    print("Resp 2 : " + str(response.status_code))
    soup = BeautifulSoup(response.text, features="lxml")

    try:
        # Get SVG tag that contains 'Profile', then get its parent
        svgs = soup.find_all('svg', attrs={"aria-label" : "Profile", "class":"simple-nav__svgIcon"})
        for svg in svgs:
            print("SVGS = " + str(svgs))
            a = svg.find_parent('a')
            print(a)
            acc = a['href'].replace('/','')
            print(acc)
    except Exception as e:
        print(e)
    break