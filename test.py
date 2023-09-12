import requests
from html.parser import HTMLParser
import pandas as pd
import re
from datetime import datetime, timedelta

from database.models import SMS
from database.database import DatabaseInterface

# url = "https://receive-smss.com/sms/33780739376/"
# headers = {
#     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 OPR/101.0.0.0'
# }
# r = requests.get(url, headers=headers)


d = datetime.now()
# hour_pattern = re.compile("[0-9]+ hour")
# tables = pd.read_html(r.text) # Returns list of all tables on page
# sp500_table = tables[0]

# print(set(l1) - set(l2))


# from database.database import DatabaseInterface
print(DatabaseInterface.sms_get_all())
