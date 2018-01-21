# -*- coding: utf-8 -*-
import scrapy
from lagou.items import LagouItem
from lagou.settings import DEFAULT_REQUEST_HEADERS, COOKIES
import time, random


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['lagou.com']
    start_urls = ['https://www.lagou.com/zhaopin/C%23/?labelWords=label']
    pn = 1
    cookie = []

    def parse(self, response):
        work_lists = response.xpath('//*[@id="s_position_list"]/ul/li')
        item = LagouItem()
        self.pn += 1
        url_next = response.xpath('//div[@class="pager_container"]/a/@href').extract()[-1] + \
                   '?filterOption={}'.format(self.pn)
        print(url_next)
        if url_next == 'javascript:;':
            return

        for work_list in work_lists:
            item['position_name'] = work_list.xpath('//a[@class="position_link"]/h3').extract()[0]
            item['position_link'] = work_list.xpath('//a[@class="position_link"]/@href').extract()[0]
            item['work_location'] = work_list.xpath('//a[@class="position_link"]/span/em/text()').extract()[0]
            item['pulish_time'] = work_list.xpath('//span[@class="format-time"]/text()').extract()[0]
            item['salary'] = work_list.xpath('//span[@class="money"]/text()').extract()[0]
            item['work_exprience'] = work_list.xpath('//div[@class="li_b_l"]/text()').extract()[2]
            item['company'] = work_list.xpath('//div[@class="company_name"]/a/text()').extract()[0]
            item['industry'] = work_list.xpath('//div[@class="industry"]/text()').extract()[0]

            yield item
        time.sleep(random.randint(2,5))
        yield scrapy.Request(url_next, headers=DEFAULT_REQUEST_HEADERS, cookies=COOKIES, callback=self.parse)

