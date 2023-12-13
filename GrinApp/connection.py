import sqlite3
import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='password',
    db='grinappdata',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
    )

cursor = conn.cursor()

class DBConnection:
    
    def queryOne(queryString):
        cursor.execute(queryString)
        return cursor.fetchone()

    def queryCommit(queryString):
        cursor.execute(queryString)
        newID = cursor.lastrowid
        conn.commit()
        return newID

    def queryAll(queryString):
        cursor.execute(queryString)
        return cursor.fetchall()
    
    def queryDescription(query):
        cursor.execute(query)
        return cursor.description