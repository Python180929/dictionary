#!/usr/bin/env python3
#coding=utf-8
'''
Name : Zhouliang
Email : 771491842@qq.com
Tel : 18301050502
Date : 2018-10-2
Class : AID1807
Project_name :  Electronic Dictionary
Env : python3
'''

from socket import *
import os
import time
import pymysql
import signal
import sys
from server import *

# 定义全局变量
HOST = '0.0.0.0'
PORT = 8000
ADDR = (HOST,PORT)


def main():
    # 创建数据库连接
    db = pymysql.connect('localhost','root','123456','dict1')
    # 创建套接字
    sockfd = socket()
    # 设置端口重用
    sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    #　绑定服务端地址
    sockfd.bind(ADDR)
    # 设置监听套接字
    sockfd.listen(5)

    # 忽略子进程信号
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)
    print('Listen the port 8000')

    # 消息接受
    while True:
        try:
            # 等待处理客户端连接
            connfd,addr = sockfd.accept()
            print("%s已连接"%addr[0])
        except KeyboardInterrupt:
            sockfd.close()
            sys.exit("服务器退出")
        except Exception as e:
            print("服务器错误是：",e)
            continue
        
        # 创建子进程
        pid = os.fork()
        if pid == 0:
            sockfd.close()
            do_child(connfd,db)
        else:
            connfd.close()
            continue

def do_child(connfd,db):
    while True:
        data = connfd.recv(1024).decode()
        print(connfd.getpeername(),':',data)
        if (not data) or (data[0] == 'E'):
            connfd.close()
            sys.exit("客户端退出")
        if data[0] == 'R':
            do_zhuce(connfd,db,data)
        if data[0] == 'D':
            do_login(connfd,db,data)
        if data[0] == 'Z':
            do_logon(connfd,db,data)
        if data[0] == 'Q':
            do_query(connfd,db,data)
        if data[0] == 'H':
            do_hist(connfd,db,data)

if __name__ == '__main__':
    main()
