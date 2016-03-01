#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import datetime
import re

from eventSpider.items.date import UnitEventDate, RepeateType, EventDate
from eventSpider.util.dateUtil import DateUtil
from eventSpider.util.locationUtil import LocationUtil

class DoubanDateUtil(DateUtil):
    ''' 
        allows to create a event date from a text string captured from web page
    '''
    @staticmethod
    def createEventDate(text):
        text = ''.join(text.split())
        # here we need use unicode, otherwise the month/day can't be recognized
        dates = re.findall(ur'(\d+\u6708\d+\u65e5)', text)        
        times = re.findall(r'(\d+:\d+)', text)

        eventDate = EventDate()
    
        currentYear = datetime.date.today().year
        if len(dates) == 1:  # we have one dates, then one-time events
            startDateMaches = (re.findall(ur'((\d+)\u6708(\d+)\u65e5)', dates[0]))
            '''
            startDate = MyDateUtil.createDate(currentYear, startDateMaches.group(0), startDateMaches.group(1))
            '''
            
            startTime = datetime.datetime.strptime(times[0], '%H:%M')
            endTime = datetime.datetime.strptime(times[1], '%H:%M')
            
            startDateTime = startTime.replace(currentYear, int(startDateMaches[0][1]), int(startDateMaches[0][2]))
            endDateTime = endTime.replace(currentYear, int(startDateMaches[0][1]), int(startDateMaches[0][2]))
    
            # UnitEventDate
            unitEventDate = UnitEventDate()
            unitEventDate['startDate'] = startDateTime
            unitEventDate['endDate'] = endDateTime
                        
            repeatType = RepeateType()
            repeatType['type'] = 0  # one time events
            # repeatType['frequency']   
            
            eventDate['unitDate'] = unitEventDate
            eventDate['repeateType'] = repeatType
     
        elif len(dates) == 2:  # we have two dates, repeatable events
            startDateMaches = re.findall(ur'((\d+)\u6708(\d+)\u65e5)', dates[0])
            endDateMaches = re.findall(ur'((\d+)\u6708(\d+)\u65e5)', dates[1])
            '''
            startDate = MyDateUtil.createDate(currentYear, int(startDateMaches[0][1]), int(startDateMaches[0][2]))
            endDate = MyDateUtil.createDate(currentYear, int(endDateMaches[0][1]), int(endDateMaches[0][2]))
            '''
            
            startTime = datetime.datetime.strptime(times[0], '%H:%M')
            endTime = datetime.datetime.strptime(times[1], '%H:%M')
    
            startDateTime = startTime.replace(currentYear, int(startDateMaches[0][1]), int(startDateMaches[0][2]))
            endDateTime = endTime.replace(currentYear, int(endDateMaches[0][1]), int(endDateMaches[0][2]))
    
            unitEventDate = UnitEventDate()
            unitEventDate['startDate'] = startDateTime
            unitEventDate['endDate'] = endDateTime
    
            repeatType = RepeateType()
            repeatType['type'] = 1  # repeatable events
            # repeatType['frequency']   
            
            eventDate['unitDate'] = unitEventDate
            eventDate['repeateType'] = repeatType
    
        else:  # not implemented yet, reserved for customized mode
            print "bad date"        
            
        return eventDate



'''
    the location ondamai.cn are in format 'address - region'
'''
class DoubanLocationUtil(LocationUtil):
        
    @staticmethod
    def getRegionAddresse(text):
        if isinstance(text, unicode):
            text = text.encode("utf-8")
        
        # remove the white spaces
        rs = re.split('-', text)
        region = ''.join(rs[1].split())
        address = ''.join(rs[0].split())
        return [region, address]
    
