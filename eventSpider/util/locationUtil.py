#!/usr/bin/env python
# -*- coding: utf-8 -*- 


from scrapy.item import Item, Field



import urllib
import json

serviceurl = 'http://api.map.baidu.com/place/v2/search?'

data = {'query':'华中科技大学', 'region':"武汉", 'output':'json', 'ak': 'sZWX5OEPWK0ezoPnFaKTfWs0'}
# data = {'query':'华中科技大学', 'region':"武汉", 'ak': 'sZWX5OEPWK0ezoPnFaKTfWs0'}
url = serviceurl + urllib.urlencode(data)

print 'Retrieving', url

uh = urllib.urlopen(url)
data = uh.read()


try: js = json.loads(str(data))



except: js = None
 
if 'status' not in js or js['status'] != 'OK':
    print '==== Failure To Retrieve ===='
 
print json.dumps(js, indent=4, ensure_ascii=False)
 