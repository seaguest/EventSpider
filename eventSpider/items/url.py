#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from scrapy.item import Item, Field

    

'''
    This object is used to filter request URL
'''
class VisitedURL(Item):
    url = Field()
    orgDupURL = Field()
    