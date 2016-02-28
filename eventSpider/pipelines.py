#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
import codecs
from eventSpider.items.url import VisitedURL

from eventSpider.util.db import DBManager
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.serialize import ScrapyJSONEncoder
_encoder = ScrapyJSONEncoder(ensure_ascii=False)

class JsonPipeline(object):
    def __init__(self):
        self.file = codecs.open('test.json', 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        # line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        line = _encoder.encode(item) + "\n";
        self.file.write(line)
        # self.file.write(_encoder.encode(line))
        return item

    def spider_closed(self, spider):
        self.file.close()
        

class DBPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings[ 'MONGODB_SERVER' ],
            settings[ 'MONGODB_PORT' ]
        )
        db = connection[settings[ 'MONGODB_DB' ]]
        self .collection = db[settings[ 'MONGODB_EVENTS' ]]


    def process_item(self , item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!" . format (data))
        if valid:
            self .collection.insert(dict (item))
            log.msg("Question added to MongoDB database!" , level=log.DEBUG, spider=spider)
        return item

    def spider_closed(self, spider):
        self.connection.close()
        
        
'''
    check the event content crawled is not duplicated with some already stored event
''' 
class DuplicatesPipeline(object):
    eventDB = DBManager(settings[ 'MONGODB_EVENTS' ])
    visitedUrlDB = DBManager(settings[ 'MONGODB_VISITED_URLS' ])

    def process_item(self, item, spider):
        if self.eventDB.exist("fingerprint", item['fingerprint']):
            """
                if the event has been stored already, then add this URL to the visited url
            """
            cursor = self.eventDB.find("fingerprint", item['fingerprint'])            
            visitedUrl = VisitedURL()
            visitedUrl['url'] = item['srcUrl']
            visitedUrl['orgDupURL'] = cursor[0]['srcUrl']
            self.visitedUrlDB.insert(visitedUrl)
            raise DropItem("Duplicate item found: %s" % item['title'])
        else:
            return item

        
class MyImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        # open("image_urls.txt","a").write(request.url + "\n")
        image_guid = request.url.split('/')[-1]
        return 'full/%s' % (image_guid)
