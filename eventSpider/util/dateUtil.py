#!/usr/bin/env python
# -*- coding: utf-8 -*- 


import datetime

from dateutil.parser import parse

class DateUtil():
    @staticmethod
    def createDate(year, month, day):
        today = datetime.date.today()
        return today.replace(year, month, day)
    @staticmethod
    def createTime(hour, minute, second):
        return datetime.time(hour, minute, second)
    @staticmethod
    def parseDate(text):
        print text
        return parse(text)
        
