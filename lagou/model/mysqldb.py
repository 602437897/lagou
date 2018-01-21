from peewee import *
from lagou.conn.mysqlconn import DBconn

dbconn = DBconn()
db = MySQLDatabase(host=dbconn.host, user=dbconn.user, password=dbconn.password, database=dbconn.database,
                   charset=dbconn.charset, port=dbconn.port)

class lagou_position_info(Model):
    position_kind = CharField(max_length=32, default='null')
    position_name = CharField(max_length=128, default='null')
    position_link = CharField(max_length=128,default='null')
    work_location = CharField(max_length=32, default='null')
    pulish_time = CharField(max_length=32, default='null')
    salary = CharField(max_length=32, default='null')
    work_exprience = CharField(max_length=32, default='null')
    company = CharField(max_length=32, default='null')
    industry = CharField(max_length=128, default='null')

    class Meta:
        database = db
        indexes = ((('position_kind', 'position_link'),True),)

