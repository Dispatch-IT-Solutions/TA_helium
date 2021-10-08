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


def getHotspotRewards(url, hotspotAddress):
    headers = {'content-type': 'application/json'}
    full_url = url + hotspotAddress + "/rewards"
    # ISO 8601 required for time search
    datemask = "%Y-%m-%dT%H:%M:%S.%fZ"
    max_time = datetime.utcnow()
    relative = timedelta(minutes=60)
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
    else:
        generateErrorReport(r)

# ------------------------
# -- Script starts here --
# ------------------------

h_hotspot_api = "https://api.helium.io/v1/hotspots/"

# Use the hotspot address within the array
hotspots = ["111111111112222222222233333334444444444444", "11111111111122222222233333333333555555555555"]

for hs in hotspots:
    getHotspotRewards(h_hotspot_api, hs)
