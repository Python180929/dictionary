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
import sys
import getpass
from client import *

def main():
    if len(sys.argv) < 3:
        print('''
            argv is error
            run as
            python3 dict_client.py 127.0.0.1 8000
            ''')
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST,PORT)

    #　创建套接字
    sockfd = socket()
    try:
        # 建立连接
        sockfd.connect(ADDR)
    except Exception as e:
        print(e)
        return
    while True:
        # os.system('clear')
        print("+------------------------------+")
        print("|           登录界面           |")
        print("|                              |")
        print("|  1)  用户注册                |")
        print("|  2)  用户登录                |")
        print("|  3)  用户注销                |")
        print("|  4)  退出                    |")
        print("+------------------------------+")

        try:
            a = int(input("请输入选项>>"))
        except Exception as e:
            print(e)
            continue
        if a not in [1,2,3,4]:
            print("输入错误，请重新输入")
            sys.stdin.flush()  # 清除标准输入
            continue
        elif a == 1:
            do_zhuce(sockfd)
        elif a == 2:
            do_login(sockfd)
        elif a == 3:
            do_logon(sockfd)
        elif a == 4:
            sockfd.send(b'E')
            sys.exit("欢迎下次使用")









if __name__ == '__main__':
    main()