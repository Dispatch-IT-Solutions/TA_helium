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
    #print("Total Seconds Difference => " + str(time_diff.total_seconds()))
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


def checkTime(lastStatusTime, difference = -3600):
    # 2021-09-07T18:43:44.481000Z
    datemask = "%Y-%m-%dT%H:%M:%S.%fZ"
    cur_time = datetime.utcnow()
    event_time = datetime.strptime(lastStatusTime, datemask)
    time_diff = event_time - cur_time
    #print("Total Seconds Difference => " + str(time_diff.total_seconds()))
    if (time_diff.total_seconds() >= difference):
        return True
    else:
        return False


def getHotspotStatus(url, hotspotAddress):
    headers = {'content-type': 'application/json'}
    full_url = url + hotspotAddress
    statusFile = '/tmp/last_' + hotspotAddress + '_status.json'
    # ISO 8601
    datemask = "%Y-%m-%dT%H:%M:%S.%fZ"
    r = requests.get(verify=True, headers = headers, url = full_url)
    if (r.status_code == 200):
        response = r.json()
        if (checkStatusTime(statusFile, 'timestamp', response['data']['status']['timestamp'])):
            if (len(response['data']) > 0):
                print(json.dumps(response['data']))
                writeStatus(statusFile, response['data']['status'])
    else:
        generateErrorReport(r)


# ------------------------
# -- Script starts here --
# ------------------------

h_hotspot_api = "https://api.helium.io/v1/hotspots/"

# Use the hotspot address within the array
hotspots = ["111111111112222222222233333334444444444444", "11111111111122222222233333333333555555555555"]

for hs in hotspots:
    getHotspotStatus(h_hotspot_api, hs)

