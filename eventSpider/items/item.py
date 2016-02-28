#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from scrapy.item import Item, Field

    
'''
	this item is used to store the craled information
'''
class EventItem(Item):
    # define the fields for your item here like:
    srcUrl = Field()
    
    title = Field()
    
    eventDate = Field()
    
    location = Field()
    
    organizer = Field()
    
    keywords = Field()
    
    descripton = Field()
    
    ''' we hash the event key words, date, location to make sure a event is unique'''
    fingerprint = Field()

    image_urls = Field()
    
    images = Field()
    
    def computeFingerprint(self):
        day = self['eventDate']['unitDate']['startDate'].timetuple().tm_yday
        return hash(day) * 1 + hash(self['location']) * 4 + hash(frozenset(self['keywords'])) * 9
