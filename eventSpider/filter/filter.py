import pymongo
from scrapy.conf import settings

from scrapy.dupefilter import RFPDupeFilter
from eventSpider.items.item import VisitedURL

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

    def insert( self , visitedUrl):
        self.collection.insert( dict (visitedUrl))

    def spider_closed(self, spider):
        self.connection.close()


'''
    customized URL fil    ter, check if the requested URL has been visited, if yes then skip.
'''
class CustomFilter(RFPDupeFilter):
    """A dupe filter that considers specific ids in the url"""
    db = DBManager(settings[ 'MONGODB_VISITED_URLS' ])

    def request_seen(self, request):
        if self.db.exist("url",request.url):
            return True
        else:
            visitedUrl = VisitedURL()
            visitedUrl['url']=request.url
            visitedUrl['orgDupURL']=None
            self.db.insert(visitedUrl)
            return False
