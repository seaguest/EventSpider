#!/usr/bin/env python
# -*- coding: utf-8 -*- 


from scrapy.item import Item, Field

'''
	The statistics that related to a event
'''
class Statistic(Item):
	pulishedDate = Field()  
	views = Field()  
	shares = Field()  
