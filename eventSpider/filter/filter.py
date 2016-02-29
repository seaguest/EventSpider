#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from scrapy.conf import settings

from scrapy.dupefilter import RFPDupeFilter
from eventSpider.items.url import VisitedURL
from eventSpider.util.db import DBManager

'''
    customized URL filter, check if the requested URL has been visited, if yes then skip.
'''
class CustomFilter(RFPDupeFilter):
    """A dupe filter that considers specific ids in the url"""
    db = DBManager(settings[ 'MONGODB_VISITED_URLS' ])

    def request_seen(self, request):
        if self.db.exist("url", request.url):
            return True
        else:
            visitedUrl = VisitedURL()
            visitedUrl['url'] = request.url
            visitedUrl['orgDupURL'] = None
            self.db.insert(visitedUrl)
            return False
