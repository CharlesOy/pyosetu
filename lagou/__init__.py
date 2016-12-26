# -*- coding: utf-8 -*-
"""
A Crawler for 拉勾网 - http://www.lagou.com/
拉勾网 is a online job search website in China, mainly for programmers and designers.
By Charles Ouyang
2016.06.24
"""

import urllib
import urllib2
import bs4
import json

# request header
req_header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4,zh-CN;q=0.2,ja;q=0.2',
    'Connection': 'close',
    'Referer': None
}


def get_soup(_request):
    """
    get soup object for a url
    :param _request:
    :return:
    """
    try:
        c = urllib2.urlopen(_request)
        return bs4.BeautifulSoup(c.read(), 'html.parser')
    except Exception, e:
        print(Exception, e)


class SearchAction:
    """
    A search action on lagou.com with all conditions allowed
    A demo url is like:
    gj=3年及以下&xl=本科&jd=天使轮&hy=移动互联网&px=default&yx=15k-25k&gx=全职&city=北京&district=朝阳区&bizArea=大山子#order
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
        DEMO URL: http://www.lagou.com/jobs/positionAjax.json?city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false
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
    TBD
    """

    def __init__(self, _position_id, _position_name=None, _position_type=None, _salary=None, _company_name=None,
                 _company_short_name=None, _company_size=None, _city=None, _district=None, _business_zones=None,
                 _company_label_list=None, _education=None, _work_year=None, _job_nature=None, _industry_field=None,
                 _create_time=None, _finance_stage=None, _position_advantage=None):
        """
        init method
        :param _position_id: position id
        :param _position_name: position name
        :param _position_type: position type
        :param _salary: salary range
        :param _company_name: company name
        :param _company_short_name: company full name
        :param _company_size: company size
        :param _city: city
        :param _district: district
        :param _business_zones: business zones
        :param _company_label_list: company label list
        :param _education: education
        :param _work_year: work year
        :param _job_nature: job type
        :param _industry_field: industry field
        :param _create_time: creating time
        :param _finance_stage: finance stage
        :param _position_advantage: position advantages
        """
        # brief info
        self.id = _position_id
        self.positionName = _position_name
        self.positionType = _position_type
        self.positionAdvantage = _position_advantage
        self.salary = _salary
        self.companyName = _company_name
        self.companyShortName = _company_short_name
        self.companySize = _company_size
        self.companyZones = _business_zones
        self.companyLabelList = _company_label_list
        self.city = _city
        self.district = _district
        self.education = _education
        self.workYear = _work_year
        self.jobNature = _job_nature
        self.industryField = _industry_field
        self.createTime = _create_time
        self.financeStage = _finance_stage
        # detailed info TBD
        self.content = 'TBD'

    def to_dic(self):
        print(dir(self))
        for entry in self:
            print(entry)
        pass


if __name__ == '__main__':

    # first=false&pn=1&kd=Python
    # kd=Python&pn=2&first=false

    sa = SearchAction('Python', '北京', _pn=1)
    print(sa.get_request().get_full_url())
    print(sa.get_request().get_data())
    print('')

    jobList = []
    for job in sa.result['positionResult']['result']:
        jobObj = Job(job['positionId'], job['positionName'], job['positionType'], job['salary'], job['companyName'],
                     job['companyShortName'], job['companySize'], job['city'], job['district'], job['businessZones'],
                     job['companyLabelList'], job['education'], job['workYear'], job['jobNature'], job['industryField'],
                     job['createTime'], job['financeStage'], job['positionAdvantage'])
        jobObj.to_dic()
        # print(jobObj.education + '\t' + jobObj.salary + '\t' + jobObj.positionName)
        # print('')
        # print(job[''])
