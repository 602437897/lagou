# -*- coding: utf-8 -*-
import scrapy
import json
from lagou.items import LagouItem
from lagou.settings import DEFAULT_REQUEST_HEADERS, COOKIES
from urllib.parse import quote


class Lagou2Spider(scrapy.Spider):
    name = 'lagou3'
    allowed_domains = ['lagou.com']
    # 页数
    pn = 1
    url = 'https://www.lagou.com/'
    k = {}

    # 第一次请求
    def start_requests(self):
        yield scrapy.FormRequest(url=self.url, headers=DEFAULT_REQUEST_HEADERS, cookies=COOKIES,
                                 callback=self.parse_kind)

    def parse_kind(self, response):
        kinds = response.xpath('//div[@class="menu_box"][1]//dl[1]/dd/a/text()')
        for i in range(2, 5):
            kinds = kinds + response.xpath('//div[@class="menu_box"][1]//dl[{}]/dd/a/text()'.format(i))

        url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false&isSchoolJob=0'

        for kind in kinds:
            kind = kind.extract().lower()
            if self.k.get(kind):
                continue
            else:
                self.k[kind] = 1
            data = {
                'first': 'false',
                'pn': str(self.k[kind]),
                'kd': kind
            }
            yield scrapy.FormRequest(url=url, headers=DEFAULT_REQUEST_HEADERS, formdata=data,
                                     cookies=COOKIES, meta={'kind': kind}, callback=self.parse)


    def parse(self, response):
        # 请求数据本身就是json串，直接存储到json中
        kind = response.meta['kind']
        try:
            d = json.loads(response.text)

            print(self.k[kind], kind)
            self.k[kind] += 1
            if self.k[kind] != 1:
                data = {
                    'first': 'false',
                    'pn': str(self.k[kind]),
                    'kd': kind
                }

            item = LagouItem()
            url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false&isSchoolJob=0'
            # 当返回成功时才去爬取数据
            if d['success'] == True:
               result = d['content']['positionResult']['result']
               if len(result) > 0:
                   for i in range(len(result)):
                       item['position_kind'] = str.lower(kind)
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
                   self.k[kind] = 1
                   yield scrapy.FormRequest(url=url, headers=DEFAULT_REQUEST_HEADERS, formdata=data, cookies=COOKIES,
                                            meta={'kind': kind}, callback=self.parse)
            else:
                # 否则返回没有获取到数据
                print(d)
                yield scrapy.FormRequest(url=url, headers=DEFAULT_REQUEST_HEADERS, formdata=data, cookies=COOKIES,
                                         meta={'kind': kind}, callback=self.parse)
            #获取下一页的数据
            yield scrapy.FormRequest(url=url, headers=DEFAULT_REQUEST_HEADERS, formdata=data, cookies=COOKIES,
                                         meta={'kind': kind}, callback=self.parse)
        except Exception as e:
            print("there is something wrong,{}".format(e))
            url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false&isSchoolJob=0'
            self.k[kind] += 1
            if self.k[kind] != 1:
                data = {
                    'first': 'false',
                    'pn': str(self.k[kind]),
                    'kd': kind
                }
                yield scrapy.FormRequest(url=url, headers=DEFAULT_REQUEST_HEADERS, formdata=data, cookies=COOKIES,
                                         meta={'kind': kind}, callback=self.parse)