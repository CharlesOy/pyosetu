# -*- coding: utf-8 -*-
"""
Test code.
"""
import json
import lagou

if __name__ == '__main__':

    # first=false&pn=1&kd=Python
    # kd=Python&pn=2&first=false

    sa = lagou.SearchAction('Python', '北京', _pn=1)
    print(sa.get_request().get_full_url())
    print(sa.get_request().get_data())
    print('')

    for job in sa.result['positionResult']['result']:
        print(job['city'])
        # print(job['companyName'])
        print(json.dumps(job['businessZones'], ensure_ascii=False))
        print(json.dumps(job['companyLabelList'], ensure_ascii=False))
        print(job['companyShortName'])
        print(job['companySize'])
        print(job['createTime'])
        print(job['district'])
        print(job['education'])
        print(job['financeStage'])
        print(job['industryField'])
        print(job['jobNature'])
        print(job['positionAdvantage'])
        print(job['positionId'])
        print(job['positionName'])
        print(job['positionType'])
        print(job['salary'])
        print(job['workYear'])
        print('')
        # print(job[''])
