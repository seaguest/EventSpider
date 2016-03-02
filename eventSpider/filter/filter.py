#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from scrapy.conf import settings

from scrapy.dupefilter import RFPDupeFilter
from eventSpider.items.url import VisitedURL
from eventSpider.util.db import DBManager

import re

'''
    customized URL filter, check if the requested URL has been visited, if yes then skip.
'''
class CustomFilter(RFPDupeFilter):
    """A dupe filter that considers specific ids in the url"""
    db = DBManager(settings[ 'MONGODB_VISITED_URLS' ])

    '''
        to avoid the requested URL http:// becomes https://, the url needs to be normalized, taken from ://
    '''
    @staticmethod
    def normalizeURL(url):
        url = ''.join(url.split())
        match = re.search(r'://(.*?)/?$', url)
        if match:
            return match.group(1)

    def request_seen(self, request):        
        normalizedUrl = CustomFilter.normalizeURL(request.url)
        if self.db.exist("url", normalizedUrl):
            return False
        else:
            visitedUrl = VisitedURL()
            visitedUrl['url'] = normalizedUrl
            visitedUrl['orgDupURL'] = None
            self.db.insert(visitedUrl)
            return False
        