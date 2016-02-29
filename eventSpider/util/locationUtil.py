#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import urllib
import json

import difflib 
import Levenshtein

from eventSpider.items.location import Location
class LocationUtil():

    @staticmethod
    def computeSimilarity(text1, text2):
        if not isinstance(text1, unicode):
            text1 = unicode(text1, "utf-8") 
        if not isinstance(text2, unicode):
            text2 = unicode(text2, "utf-8") 
        return difflib.SequenceMatcher(None, text1, text2).ratio()

    '''
        a text match candidate, seems the same as above
    '''
    @staticmethod
    def computeSimilarity2(text1, text2):
        if not isinstance(text1, unicode):
            text1 = unicode(text1, "utf-8") 
        if not isinstance(text2, unicode):
            text2 = unicode(text2, "utf-8") 
        return Levenshtein.ratio(text1, text2)

    @staticmethod
    def getPOIs(region, address):
        serviceurl = 'http://api.map.baidu.com/place/v2/search?'
        data = {'region':region, 'query':address, 'output':'json', 'ak': 'sZWX5OEPWK0ezoPnFaKTfWs0'}
        url = serviceurl + urllib.urlencode(data)
        uh = urllib.urlopen(url)
        data = uh.read()
        try: js = json.loads(str(data))
        except: js = None
        
        # print json.dumps(js, indent=4, ensure_ascii=False)

        if 'status' not in js or js['status'] != 0:
            print '==== Failure To Retrieve ===='
        return js

    @staticmethod
    def getBestMatchedPOI(region, address):
        # in case the similarity is less than 0.5, return None
        maxSimilarity = 0.5
        bestMatchedPOI = None
        js = LocationUtil.getPOIs(region, address)
        

        for record in js['results']:
            currentSimilarity = LocationUtil.computeSimilarity(record['name'], address),
            if currentSimilarity > maxSimilarity:
                maxSimilarity = currentSimilarity
                bestMatchedPOI = record
            
        return bestMatchedPOI    


    @staticmethod
    def createLocation(region, address):
        location = Location()
        location['region'] = region
        matchedPOI = LocationUtil.getBestMatchedPOI(region, address)
        
        # print json.dumps(matchedPOI, indent=4, ensure_ascii=False)

        if matchedPOI:
            location['name'] = matchedPOI['name']
            location['address'] = matchedPOI['address']
        location['name'] = address

        return location
