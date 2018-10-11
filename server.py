from socket import *
import os
import time
import pymysql
import signal
import sys
from server import *

def do_zhuce(connfd,db,data):
    print("注册操作")
    l = data.split(' ')
    name = l[1]
    passwd = l[2]
    # 创建游标对象
    cursor = db.cursor()
    sql_select = "select * from user where name='%s'"%name
    cursor.execute(sql_select)
    db.commit()
    r = cursor.fetchone()
    if r != None:
        connfd.send(b'EXIST')
        return
    # 将用户名存入数据库
    sql_insert = "insert into user (name,passwd) \
    values ('%s','%s')"%(name,passwd)
    try:
        cursor.execute(sql_insert)
        db.commit()
        connfd.send(b'OK')
    except:
        db.rollback()
        connfd.send(b'FALL')
    else:
        print("%s注册成功"%name)

def do_login(connfd,db,data):
    print("登录操作")
    l = data.split(' ')
    name = l[1]
    passwd = l[2]
    # 创建游标对象
    cursor = db.cursor()
    sql_select = "select name,passwd from user where name='%s' \
                and passwd='%s'"%(name,passwd)
    cursor.execute(sql_select)
    db.commit()
    r = cursor.fetchone()
    if r == None:
        connfd.send(b'N')
    else:
        print("%s登录成功"%name)
        connfd.send(b'OK')

def do_logon(connfd,db,data):
    print("注销操作")
    l = data.split(' ')
    name = l[1]
    passwd = l[2]
    #创建游标对象
    cursor = db.cursor()
    sql_select = "select name,passwd from user where name='%s' \
                and passwd='%s'"%(name,passwd)
    cursor.execute(sql_select)
    db.commit()
    r = cursor.fetchone()
    if r == None:
        connfd.send(b'N')
        return
    sql_delete = "delete from user where name='%s' \
                and passwd='%s'"%(name,passwd)
    try:
        cursor.execute(sql_delete)
        db.commit()
        connfd.send(b'OK')
    except:
        db.rollback()
        connfd.send(b'FALL')
    else:
        print("%s注销成功"%name)

def do_query(connfd,db,data):
    print("单词查询")
    l = data.split(' ')
    name = l[1]
    word = l[2]
    cursor = db.cursor()
    sql_select = "select jieshi from words where word='%s'"%word
    cursor.execute(sql_select)
    db.commit()
    r = cursor.fetchone()
    if r != None:
        connfd.send(b'OK')
        time.sleep(0.1)
        for i in r:
            connfd.send(i.encode())
        sql_insert = "insert into hist (name,word) values \
                ('%s','%s')"%(name,word)
        try:
            cursor.execute(sql_insert)
            db.commit()
        except:
            db.rollback()
    else:
        connfd.send(b'FALL')

def do_hist(connfd,db,data):
    print("历史记录查询")
    l = data.split(' ')
    name = l[1]
    cursor = db.cursor()
    sql_select = "select * from hist where name='%s'"%name
    cursor.execute(sql_select)
    db.commit()
    r = cursor.fetchall()
    if r != None:
        connfd.send(b'OK')
        for i in r:
            time.sleep(0.1)
            msg = "%s      %s      %s"%(i[1],i[2],i[3])
            connfd.send(msg.encode())
        time.sleep(0.1)
        connfd.send(b'##')
    else:
        connfd.send(b'FALL')

