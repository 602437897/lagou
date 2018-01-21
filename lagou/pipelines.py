# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from lagou.conn import mongodbconn
from pymongo import ASCENDING
from lagou.conn import mysqlconn
from lagou.model import mysqldb
from lagou.model.mysqldb import lagou_position_info

# 存储到本地的json文件中
class LagouPipeline(object):
    def __init__(self):
        self.f = open("lagou.json", "w")

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + ',\n'
        self.f.write(content)
        return item

    def close_spider(self, spider):
        self.f.close()

# 存储到mongodb数据库中
class LagouMongoPipeline(object):
    # 创建数据库连接
    def __init__(self):
        db_conn = mongodbconn.DBconn()
        self.conn = db_conn.connect()
        self.db = self.conn.mydb

    def process_item(self, item, spider):
        item = dict(item)

        my_set = self.db.lagou
        """ 
        因为职位对应的职位详细的链接地址肯定是惟一的,所以考虑将职位链接作为唯一索引,只有当职位链接在当前数据库中
        不存在的情况下才将数据插入
        """
        for i in my_set.find({"position_link": item["position_link"], "position_kind": item["position_kind"]}):
            print(len(i))
            if len(i) >= 10:
                print("find it,{},{}".format(item["position_kind"], item["position_link"]))
                return item
        """
        因为mongodb本身集合创建时惰性的,所以第一次进来的时候因为一条数据都没有,所以其实这时候集合是不存在的,
        所以需要将进来的第一条数据插进集合中,这样后续才能保证my_set.find正常执行，同时创建唯一索引。
       """
        print("get it,{},{}".format(item["position_kind"], item["position_link"]))
        my_set.insert(dict(item))
        my_set.create_index([("position_link", ASCENDING),("position_kind", ASCENDING)],unique=True)

        return item

    # 关闭数据库连接
    def close_spider(self, spider):
        self.conn.close()


class LagouMysqlPipeline(object):
    def __init__(self):
        try:
            mysqldb.db.create_tables([lagou_position_info])
            mysqldb.db.connect()
        except Exception as e:
            print(e)

    def process_item(self, item, spider):
        item = dict(item)
        if lagou_position_info.select().where(lagou_position_info.position_kind == item['position_kind'],
                                              lagou_position_info.position_link == item['position_link']):
            print("find it,{},{}".format(item["position_kind"], item["position_link"]))
            return item
        else:
            position = lagou_position_info(position_kind=item['position_kind'],
                                           position_name=item['position_name'],
                                           position_link=item['position_link'],
                                           work_location=item['work_location'],
                                           pulish_time=item['pulish_time'],
                                           salary=item['salary'],
                                           work_exprience=item['work_exprience'],
                                           company=item['company'],
                                           industry=item['industry'])

            position.save()
            return item


    def close_spider(self, spider):
        mysqldb.db.close()



