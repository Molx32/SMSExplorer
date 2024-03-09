import requests
import re
import csv
requests.packages.urllib3.disable_warnings()
import json

with open('data.csv', 'r', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        domain      = row[0]
        interest    = row[1]
        interestd   = row[2]

        is_interesting = False
        is_automated = False
        is_interesting_desc = []
        if interest == "NOK" and interestd == "NOK":
            is_interesting_desc.append("DATA_INTERESTING_DESC_NO_OTHER")
        elif interest == "SCAM":
            if interestd == "SCAM":
                is_interesting_desc.append("DATA_INTERESTING_DESC_NO_SCAM")
            if interestd == "AD":
                is_interesting_desc.append("DATA_INTERESTING_DESC_NO_AD")
            if interestd == "SCAM/AD":
                is_interesting_desc.append("DATA_INTERESTING_DESC_NO_AD")
                is_interesting_desc.append("DATA_INTERESTING_DESC_NO_SCAM")
        elif interest == "Interest":
            is_interesting = True
            if interestd == "Automated":
                is_automated = True
            if interestd == "PII":
                is_interesting_desc.append("DATA_INTERESTING_DESC_YES_PII")
            else:
                continue
        elif interest == "Missed opportunity":
            is_interesting_desc.append("DATA_INTERESTING_DESC_NO_MISSED_OPPORTUNITY")
        else:
            continue

        if len(is_interesting_desc) == 1:
            is_interesting_desc_str = '"' + is_interesting_desc[0] + '"'
        else:
            is_interesting_desc_str = '"' + '","'.join(is_interesting_desc) + '"'
        item = \
        '''
            {
                "domain":"''' + domain + '''",
                "is_automated":''' + str(is_automated) + ''',
                "is_interesting":''' + str(is_interesting) + ''',
                "is_interesting_desc":[''' + is_interesting_desc_str + ''']
            },'''


        print(item)