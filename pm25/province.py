#!/usr/bin/env python
# encoding: utf-8

import requests

url = "http://apis.baidu.com/3023/weather/province"

headers = {
    'apikey':'fb655c55aed101b68d2e1f3bf5534738',
}

response = requests.get(url, headers=headers)
print response.json()
for d in response.json():
    print d[0], d[1]

