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
    
    category = Field()
    
    # indicate if the event is private or public 
    private = Field()
    
    # indicate the price, 0 means free
    expense = Field()
    
    # the maximum number of participant 
    maxParticipant = Field()
    
    # list of participant id
    participants = Field()
    
    # list of interested user id
    interested = Field()

    # list of comment
    comments = Field()
    
    # number of ThumbUp
    nbThumUps = Field()

    # the valuation from user
    star = Field()

    # synthetical popularity
    popularity = Field()
    
    keywords = Field()
    
    description = Field()
    
    ''' we hash the event key words, date, location to make sure a event is unique'''
    fingerprint = Field()

    image_urls = Field()
    
    images = Field()
    
    def computeFingerprint(self):
        day = 0
        if 'eventDate' in self and 'unitDate' in self['eventDate'] and 'startDate' in self['eventDate']['unitDate']:
            day = self['eventDate']['unitDate']['startDate'].timetuple().tm_yday
        return hash(day) * 1 + hash(self['location']['name']) * 4 + hash(frozenset(self['keywords'])) * 9
