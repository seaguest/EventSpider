#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import pymongo
from scrapy.conf import settings


'''
    A basic MongoDB Manaher
'''
class DBManager(object):
    def __init__(self, collection):
        connection = pymongo.MongoClient(
            settings[ 'MONGODB_SERVER' ],
            settings[ 'MONGODB_PORT' ]
        )
        db = connection[settings[ 'MONGODB_DB' ]]
        self.collection = db[collection]


    def find(self , name, value):
        cursor = self.collection.find({name:value})
        return cursor

    def exist(self , name, value):
        cursor = self.find(name, value)
        if cursor.count() > 0:
            return True
        else:
            return False

    def insert(self , visitedUrl):
        self.collection.insert(dict (visitedUrl))

    def spider_closed(self, spider):
        self.connection.close()
