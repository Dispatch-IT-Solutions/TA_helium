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


def getOraclePrice():
    headers = {'content-type': 'application/json'}
    full_url = 'https://api.helium.io/v1/oracle/prices/current'
    r = requests.get(verify=True, headers = headers, url = full_url)
    if (r.status_code == 200):
        print(json.dumps(r.json()['data']))

def checkTime(lastStatusTime):
    printEvent = False
    # 2021-09-07T18:43:44.481000Z
    datemask = "%Y-%m-%dT%H:%M:%S.%fZ"
    cur_time = datetime.utcnow()
    event_time = datetime.strptime(lastStatusTime, datemask)
    time_diff = event_time - cur_time
    if (time_diff.total_seconds() > -7200):
        #If last update was less than 2 hours ago
        printEvent = True
    return printEvent

def getHotspotStatus(url, hotspotAddress):
    headers = {'content-type': 'application/json'}
    full_url = url + hotspotAddress
    # ISO 8601
    datemask = "%Y-%m-%dT%H:%M:%S.%fZ"
    r = requests.get(verify=True, headers = headers, url = full_url)
    if (r.status_code == 200):
        if (checkTime(r.json()['data']['status']['timestamp'])):
            print(json.dumps(r.json()['data']))


def getHotspotRewards(url, hotspotAddress):
    headers = {'content-type': 'application/json'}
    full_url = url + hotspotAddress + "/rewards"
    # ISO 8601 required for time search
    datemask = "%Y-%m-%dT%H:%M:%S.%fZ"
    max_time = datetime.utcnow()
    relative = timedelta(minutes=120)
    min_time = max_time - relative
    max_time_str = datetime.strftime(max_time, datemask) 
    min_time_str = datetime.strftime(min_time, datemask)
    # Creating the parameters for time window
    initial_search = {'min_time': min_time_str, 'max_time': max_time_str}
    r = requests.get(verify=True, headers = headers, url = full_url, params=initial_search)
    if (r.status_code == 200):
        response = r.json()
        # If only one response, it tends to include it here along with a 'cursor' for some reason
        if (len(response['data']) > 0):
            print(json.dumps(response['data'][0]))
        # May need to page through the results
        if 'cursor' in response:
            page = {'cursor': response['cursor']}
            results = requests.get(verify=True, headers = headers, url = full_url, params=page)
            if (results.status_code == 200):
                for reward in results.json()['data']:
                    print(json.dumps(reward))

# ------------------------
# -- Script starts here --
# ------------------------

h_hotspot_api = "https://api.helium.io/v1/hotspots/"

# Use the hotspot address within the array
hotspots = ["0000000000000000001111111111111111111111111111111111"]

for hs in hotspots:
    getOraclePrice()
    getHotspotStatus(h_hotspot_api, hs)
    getHotspotRewards(h_hotspot_api, hs)


