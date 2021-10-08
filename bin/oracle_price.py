from __future__ import print_function
from builtins import str
import os
import sys
from time import localtime,strftime
from datetime import timedelta
from datetime import datetime
import time
import json
import requests


def generateErrorReport(error_payload):
    print("ERROR => " + error_payload.text)


def writeStatus(fileName, data):
    with open(fileName, 'w') as outfile:
        json.dump(data, outfile)


# Returns 'True' if 'timeTwo' is later than 'timeOne'
def timeDifference(timeOne, timeTwo):
    # 2021-09-07T18:43:44.481000Z
    datemask = "%Y-%m-%dT%H:%M:%S.%fZ"
    p_time = datetime.strptime(timeOne, datemask)
    l_time = datetime.strptime(timeTwo, datemask)
    time_diff = l_time - p_time
    ret_value = False
    if (time_diff.total_seconds() > 0.0):
        return True
    else:
        return False


def checkStatusTime(fileName, keyName, latestTime):
    try:
        with open(fileName) as open_file:
            contents = json.load(open_file)
            timeDifference(contents[keyName], latestTime)
    except FileNotFoundError:
        # If the file does not exist, we assume it is the latest time
        return True


def getOraclePrice():
    headers = {'content-type': 'application/json'}
    full_url = 'https://api.helium.io/v1/oracle/prices/current'
    statusFile = '/tmp/last_oracle_price.json'
    r = requests.get(verify=True, headers = headers, url = full_url)
    if (r.status_code == 200):
        if (checkStatusTime(statusFile, 'timestamp', r.json()['data']['timestamp'])):
            print(json.dumps(r.json()['data']))
            writeStatus(statusFile, r.json()['data'])
    else:
        generateErrorReport(r)


# ------------------------
# -- Script starts here --
# ------------------------

# Pull the most recent Oracle price
getOraclePrice()

