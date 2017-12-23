import pymysql.cursors


class DBConnection():
    #get MySQL DB connection
    def getConnection(self):
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='',
                                     db='adist',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection
