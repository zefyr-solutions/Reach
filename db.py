import pymysql

def connect():
    connection = pymysql.connect(host='127.0.0.1',
                             user='user',
                             password='pass',
                             db='malayil')
    return connection
