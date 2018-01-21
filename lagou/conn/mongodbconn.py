import pymongo

# 数据库连接
class DBconn:
    def __init__(self):
        self.conn = None
        self.server_IP = '127.0.0.1'
        self.server_port = 27017

    def connect(self):
        return pymongo.MongoClient(self.server_IP, self.server_port)

    def close(self):
        return self.conn.close()
