#!/usr/bin/env python
# -*- coding: utf-8 -*- 


from scrapy.item import Item, Field



import urllib
import json

serviceurl = 'http://api.map.baidu.com/place/v2/search?'

data = {'query':'华中科技大学', 'region':"武汉",'ak': 'E4805d16520de693a3fe707cdc962045'}
url = serviceurl + urllib.urlencode(data)

print 'Retrieving', url
uh = urllib.urlopen(url)
data = uh.read()
print 'Retrieved',len(data),'characters'

try: js = json.loads(str(data))
except: js = None
if 'status' not in js or js['status'] != 'OK':
    print '==== Failure To Retrieve ===='
    print data
 
print json.dumps(js, indent=4)

lat = js["results"][0]["geometry"]["location"]["lat"]
lng = js["results"][0]["geometry"]["location"]["lng"]
print 'lat',lat,'lng',lng
location = js['results'][0]['formatted_address']
print location