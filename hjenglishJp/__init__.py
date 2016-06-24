# -*- coding: utf-8 -*-
"""
A Crawler for 沪江小D - http://dict.hjenglish.com/jp/
沪江小D is a online Japanese-Chinese dictionary.
By Charles Ouyang
2016.06.24
"""

import urllib2
import bs4


class Word:
    """
    Basic unit of a dictionary
    """

    def __init__(self, _japanese):
        self.japanese = _japanese
        pass

    def translate(self):
        url = 'http://dict.hjenglish.com/services/simpleExplain/jp_simpleExplain.ashx?type=jc&w=' + self.japanese
        pass