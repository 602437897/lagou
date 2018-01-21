# -*- coding: utf-8 -*-
import scrapy
import json
from lagou.items import LagouItem
from lagou.settings import DEFAULT_REQUEST_HEADERS, COOKIES
from urllib.parse import quote


class Lagou2Spider(scrapy.Spider):
    name = 'lagou2'
    allowed_domains = ['lagou.com']
    # 页数
    pn = 1
    url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false&isSchoolJob=0'
    kd = 'Python'
    # 请求数据
    data = {
        'first': 'true',
        'pn': str(pn),
        'kd': kd
    }
    DEFAULT_REQUEST_HEADERS['Referer'] = 'https://www.lagou.com/jobs/list_{}?labelWords=&fromSearch=true&suginput='.format(quote(kd))
    # 第一次请求
    def start_requests(self):
        yield scrapy.FormRequest(url=self.url, headers=DEFAULT_REQUEST_HEADERS, formdata=self.data, cookies=COOKIES,
                                 callback=self.parse)


    def parse(self, response):
        # 请求数据本身就是json串，直接存储到json中
        d = json.loads(response.text)
        item = LagouItem()
        # 当返回成功时才去爬取数据
        if d['success'] == True:
           result = d['content']['positionResult']['result']
           if len(result) > 0:
               for i in range(len(result)):
                   item['position_kind'] = 'Python'
                   item['position_name'] = result[i]['positionName']
                   item['position_link'] = 'https://www.lagou.com/jobs/{}.html'.format(result[i]['positionId'])
                   item['work_location'] = result[i]['city']
                   item['pulish_time'] = result[i]['createTime']
                   item['salary'] = result[i]['salary']
                   item['work_exprience'] = result[i]['workYear']
                   item['company'] = result[i]['companyShortName']
                   item['industry'] = result[i]['industryField']

                   yield item
           else:
               print(d)
               return
        else:
            # 否则返回没有获取到数据
            print(d)
            return
        #获取下一页的数据
        self.pn += 1
        if self.pn != 1:
            self.data['first'] = 'false'
            self.data['pn'] = str(self.pn)
            print(self.pn)
            yield scrapy.FormRequest(url=self.url, headers=DEFAULT_REQUEST_HEADERS, formdata=self.data, cookies=COOKIES,
                                 callback=self.parse)