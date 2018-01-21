import pymysql

class DBconn:
    def __init__(self):
        self.host = '127.0.0.1'
        self.user = 'root'
        self.password = 'root'
        self.database = 'test'
        self.charset = 'gbk'
        self.port = 3306