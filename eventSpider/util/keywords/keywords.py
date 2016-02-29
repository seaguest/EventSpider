#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#jieba.load_userdict("userdict.txt")
import jieba.analyse

import sys
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

class keyWordGenerator():
    @staticmethod
    def generateKeywords(text):
        #seg_list = jieba.cut(text, cut_all=True)
        seg_list = jieba.analyse.extract_tags(text, 5) # 默认是精确模式

        return seg_list

