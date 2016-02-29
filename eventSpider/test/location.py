#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import json

from eventSpider.util.locationUtil import LocationUtil


region = "上海"
address = "上海体育馆"

js = LocationUtil.getPOIs(region, address)
print json.dumps(js, indent=4, ensure_ascii=False)

for record in js['results']:
    print address, record['name'], LocationUtil.computeSimilarity(record['name'], address)

 
find = LocationUtil.createLocation(region, address)

print repr(find)
print type(find['name'])

print find['address'] 


print unicode(find['name'], "utf-8")
print find['address']
print unicode(find['region'], "utf-8")

# print find['name'].encode("utf-8")

# print json.dumps(find, indent=4, ensure_ascii=False)
