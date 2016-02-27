#!/usr/bin/env python
# -*- coding: utf-8 -*- 


from scrapy.item import Item, Field

class Location(Item):
	name = Field()	# title of the place
	region = Field()	#region, city or province
	address = Field()	# detailed address
	details = Field()	# description details, building...etc
