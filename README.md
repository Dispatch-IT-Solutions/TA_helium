### Technology Add-On for Helium

This TA will grab the following details (if applicable) on the interval you set
- Oracle Price
- Hotspot Status (location, network status, listen address(es), etc.)
- Hotspot Rewards

#### ./default/inputs.conf
```
[script://./bin/hotspot_checker.py]
interval = 0 */2 * * *
sourcetype = _json
source = helium_api
disabled = 0
python.version = python3
```

#### Make sure to update the python script with your hotspot address(es)
```
...
    # Single hotspot example
    hotspots = ["0000000000000000000001111111111111111111122222222222"]
    # Multiple hotspots example
    hotspots = ["0000000000000000000001111111111111111111122222222222", "3333333333333333333334444444444444444444444444444444"]
...
```

System Requirements : Python 3.7 or greater
App Developer       : Adam Saul
Version Support     : app_support@dispatchitsolutions.io

Disclaimer:
This app is not endorsed by, directly affiliated with, maintained, authorized, or sponsored by Helium.
