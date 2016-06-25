# -*- coding: utf-8 -*-
"""
A Crawler for 拉勾网 - http://www.lagou.com/
拉勾网 is a online job search website in China, mainly for programmers and designers.
By Charles Ouyang
2016.06.24
"""

import urllib
import urllib2
import json

# request header
req_header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4,zh-CN;q=0.2,ja;q=0.2',
    'Connection': 'close',
    'Referer': None
}


class SearchAction:
    """
    A search action on lagou.com with all conditions allowed
    """

    def __init__(self, _kd, _city, _district=None, _gj=None, _xl=None, _jd=None, _hy=None, _yx=None, _gx=None, _px=None,
                 _pn=1):
        """
        init method
        :param _kd: keyword
        :param _city: city
        :param _district: district
        :param _gj: working experience
        :param _xl: education
        :param _jd: finance phrase
        :param _hy: industry
        :param _yx: salary
        :param _gx: job type
        :param _px: order
        :param _pn: page number
        """
        # form data
        self.form = {}
        self.form.setdefault('first', 'false')
        self.form.setdefault('pn', _pn)
        self.form.setdefault('kd', _kd)
        # query string data
        self.query_string = {}
        self.query_string.setdefault('city', _city)
        self.query_string.setdefault('district', _district)
        self.query_string.setdefault('gj', _gj)
        self.query_string.setdefault('xl', _xl)
        self.query_string.setdefault('jd', _jd)
        self.query_string.setdefault('hy', _hy)
        self.query_string.setdefault('yx', _yx)
        self.query_string.setdefault('gx', _gx)
        self.query_string.setdefault('px', _px)

        # parse response string, which is a json object, to a dictionary
        # what we need is in 'content'
        # raw string
        result = urllib2.urlopen(self.get_request()).read()
        # convert raw string to a dictionary
        result = json.loads(result)['content']
        self.result = result

    def __str__(self):
        """
        to string
        :return:
        """
        string = ''
        for index, entry in enumerate(self.query_string):
            string += entry + '=' + str(self.query_string[entry]) + '&'
        string += 'needAddtionalResult=false'
        return str({'query_string': string, 'form': self.form}).decode('utf-8')

    def get_request(self):
        """
        produce request
        # http://www.lagou.com/jobs/positionAjax.json?city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false
        :return:
        """
        url = 'http://www.lagou.com/jobs/positionAjax.json?'
        for index, entry in enumerate(self.query_string):
            if self.query_string[entry] is not None:
                url += entry + '=' + self.query_string[entry] + '&'
        url += 'needAddtionalResult=false'
        return urllib2.Request(url, urllib.urlencode(self.form), req_header)


class Job:
    """
    Detailed job info
    """

    def __init__(self, id):
        """
        init method
        """
        pass
