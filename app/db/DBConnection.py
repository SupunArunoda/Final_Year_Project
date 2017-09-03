import pymysql.cursors


class DBConnection():
    def getConnection(self):
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='',
                                     db='adist',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection
