# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 职位类别
    position_kind = scrapy.Field()

    # 职位名称
    position_name = scrapy.Field()

    # 职位链接
    position_link = scrapy.Field()

    # 工作地点
    work_location = scrapy.Field()

    # 发布时间
    pulish_time = scrapy.Field()

    # 工资
    salary = scrapy.Field()

    # 工作经验
    work_exprience = scrapy.Field()

    # 招聘公司名称
    company = scrapy.Field()

    # 行业
    industry = scrapy.Field()
