#!/usr/bin/env python
# -*- coding: utf-8 -*- 


from scrapy.item import Item, Field

class EventDate(Item):
	unitDate = Field()
	repeateType = Field()
	dates = Field()	# list of all UnitEventDate, calculated based on unitEventDate and repeatMode

'''
	UnitEventDate should be combined with RepeateType
	i.e if date is 2017/01/01 09:00 - 2017/01/03 17:00 
			if repeateTYpe.type = 0
				then this is a one-time event during 3 days
			if repeateTYpe.type = 1
				then this is a repeatable event from 09:00-17:00 for certain days determined by the frequency
			if repeateTYpe.type = 2
				then this is a customized event, we need to check EventDate.dates
'''
class UnitEventDate(Item):
	# define the basic unit date for event 
	startDate = Field()	# datetime.datetime format
	endDate = Field()	# datetime.datetime format

class RepeateType(Item):
	# define the repeat mode 				
	# 	0:one-time event
	# 	1:repeatable
	# 	2:customizable
	type = Field()		
	frequency = Field()		# {0,1,2,3,4,5,6}
