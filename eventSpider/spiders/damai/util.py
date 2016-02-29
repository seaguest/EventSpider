#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import re

from eventSpider.items.date import UnitEventDate, RepeateType, EventDate
from eventSpider.util.dateUtil import DateUtil
from eventSpider.util.locationUtil import LocationUtil

class DamaiDateUtil(DateUtil):
    
    @staticmethod
    def isValidDate(text):
        text = ''.join(text.split())
        # suppose all dates contains (\d+)-(\d+) or (\d+):(\d+)
        matches = re.findall(r'(\d+)-(\d+)|(\d+):(\d+)', text) 
        return len(matches) != 0
    
    
    '''
        Damai events are almost one-time events
    '''
    @staticmethod
    def createEventDate(dateList):
        eventDate = EventDate()

        if len(dateList) == 1:
            startDate = DamaiDateUtil.createDate(dateList[0])
            unitEventDate = UnitEventDate()
            unitEventDate['startDate'] = startDate
                         
            repeatType = RepeateType()
            repeatType['type'] = 0  # one time events
            
            eventDate['unitDate'] = unitEventDate
            eventDate['repeateType'] = repeatType

        # if we have everal dates, repeatable but customized events
        if len(dateList) > 1:
            eventDate['dates'] = []
            for i in range(len(dateList)):
                startDate = DamaiDateUtil.createDate(dateList[i])
                unitEventDate = UnitEventDate()
                unitEventDate['startDate'] = startDate
                eventDate['dates'].append(unitEventDate)
                if i == 0:
                    eventDate['unitDate'] = unitEventDate

            repeatType = RepeateType()
            repeatType['type'] = 2  # customized events 
            
            eventDate['repeateType'] = repeatType
        return eventDate

    @staticmethod
    def createDate(date):
        normalizedDate = re.sub(r'[^\d]', '', date)
        startDate = DamaiDateUtil.parseDate(normalizedDate)
        return startDate
    

'''
    the location ondamai.cn are in format 'address - region'
'''
class DamaiLocationUtil(LocationUtil):
        
    @staticmethod
    def getRegionAddresse(text):
        if isinstance(text, unicode):
            text = text.encode("utf-8")
        
        # remove the white spaces
        rs = re.split('-', text)
        region = ''.join(rs[1].split())
        address = ''.join(rs[0].split())
        return [region, address]
    
