import json
import sys


DATA_AUTOMATED_YES                                  = []
DATA_AUTOMATED_NO                                   = []
DATA_INTERESTING_YES                                = []
DATA_INTERESTING_NO                                 = []
DATA_INTERESTING_DESC_NO_SCAM                       = []
DATA_INTERESTING_DESC_NO_AD                         = []
DATA_INTERESTING_DESC_NO_MISSED_OPPORTUNITY         = []
DATA_INTERESTING_DESC_NO_OTHER                      = []
DATA_INTERESTING_DESC_NO_OTHER                      = []
DATA_INTERESTING_DESC_YES_PII                       = []
DATA_INTERESTING_DESC_YES_DISCOVERY                 = []
DATA_INTERESTING_DESC_YES_ACCOUNT_TAKEOVER          = []
DATA_INTERESTING_DESC_YES_ACCOUNT_PASSWORD_RESET    = []

with open('config.json', 'r') as f:
    data = json.load(f)
    for item in data['data']:

        # AUTOMATED
        if item['is_automated'] == True:
            DATA_AUTOMATED_YES.append(item['domain'])
        else: 
            DATA_AUTOMATED_NO.append(item['domain'])

        # INTERESING
        if item['is_interesting'] == True:
            DATA_INTERESTING_YES.append(item['domain'])
        else: 
            DATA_INTERESTING_NO.append(item['domain'])

        # NO INTERESING DESC 
        if "DATA_INTERESTING_DESC_NO_SCAM"                 in item['is_interesting_desc']:
            DATA_INTERESTING_DESC_NO_SCAM.append(item['domain'])
        if "DATA_INTERESTING_DESC_NO_AD"                   in item['is_interesting_desc']:
            DATA_INTERESTING_DESC_NO_AD.append(item['domain'])
        if "DATA_INTERESTING_DESC_NO_MISSED_OPPORTUNITY"   in item['is_interesting_desc']:
            DATA_INTERESTING_DESC_NO_MISSED_OPPORTUNITY.append(item['domain'])
        if "DATA_INTERESTING_DESC_NO_OTHER"                in item['is_interesting_desc']:
            DATA_INTERESTING_DESC_NO_OTHER.append(item['domain'])
        if "DATA_INTERESTING_DESC_NO_OTHER"                in item['is_interesting_desc']:
            DATA_INTERESTING_DESC_NO_OTHER.append(item['domain'])

        # INTERESING DESC 
        if "DATA_INTERESTING_DESC_YES_PII"                                      in item['is_interesting_desc']:
            DATA_INTERESTING_DESC_YES_PII.append(item['domain'])
        if "DATA_INTERESTING_DESC_YES_DISCOVERY"                                in item['is_interesting_desc']:
            DATA_INTERESTING_DESC_YES_DISCOVERY.append(item['domain'])
        if "DATA_INTERESTING_DESC_YES_ACCOUNT_TAKEOVER"                         in item['is_interesting_desc']:
            DATA_INTERESTING_DESC_YES_ACCOUNT_TAKEOVER.append(item['domain'])
        if "DATA_INTERESTING_DESC_YES_ACCOUNT_PASSWORD_RESET"                   in item['is_interesting_desc']:
            DATA_INTERESTING_DESC_YES_ACCOUNT_PASSWORD_RESET.append(item['domain'])