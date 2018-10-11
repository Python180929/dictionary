from socket import *
import os
import sys
import getpass
from client import *
# 注册
def do_zhuce(sockfd):
    while True:
        name = input("请输入用户名")
        if not name:
            print("用户名不能为空")
            continue
        elif name == '##':
            break
        passwd = getpass.getpass()
        if (not passwd) or (' ' in passwd):
            print("密码不能为空或密码中不能包含空格")
            continue
        passwd1 = getpass.getpass("Again Password")
        if passwd != passwd1:
            print("两次密码不一致")
            continue 
        cmg = 'R {} {}'.format(name,passwd)
        sockfd.send(cmg.encode())
        data = sockfd.recv(128).decode()
        if data == 'OK':
            print("注册成功")
            # login(sockfd,name)　　# 进入二级界面
            break
        elif data == "EXIST":
            print("用户名已存在")
        else:
            print("注册失败")

def do_login(sockfd):
    while True:
        name = input("User:")
        if name == '##':
            break
        passwd = getpass.getpass()
        cmg = 'D {} {}'.format(name,passwd)
        sockfd.send(cmg.encode())
        data = sockfd.recv(128).decode()
        if data == 'OK':
            print("登录成功")
            login(sockfd,name) # 进入二级界面
            return
        if data == 'N':
            print("用户不存在或密码错误")
        else:
            print("登录失败")

def do_logon(sockfd):
    name = input("User:")
    passwd = getpass.getpass()
    cmg = 'Z {} {}'.format(name,passwd)
    sockfd.send(cmg.encode())
    data = sockfd.recv(128).decode()
    if data == 'OK':
        print("注销成功")
        return
    if data == 'N':
        print("用户不存在")
    else:
        print("注销失败")

def login(sockfd,name):
    while True:
        # os.system("clear")
        print("+-------------------------------+")
        print("|          查询界面         　  |")
        print("|                               |")
        print("|  1)   单词查询                |")
        print("|  2)   历史记录查询            |")
        print("|  3)   退出                    |")
        print("+-------------------------------+") 

        try:
            a = int(input("请输入选项>>"))
        except Exception as e:
            print(e)
            continue
        if a not in [1,2,3]:
            print("输入错误，请重新输入")
            sys.stdin.flush()  # 清除标准输入
            continue 
        elif a == 1:
            do_query(sockfd,name) 
        elif a == 2:
            do_hist(sockfd,name)
        elif a == 3:
            break     

def do_query(sockfd,name):
    while True:
        word = input("单词>>")
        if word == '##':
            break
        msg = "Q {} {}".format(name,word)
        sockfd.send(msg.encode())
        data = sockfd.recv(128).decode()
        if data == "OK":
            data = sockfd.recv(2048).decode()
            print(data)
        else:
            print("没有找到这个单词")

def do_hist(sockfd,name):
    msg = "H {}".format(name)
    sockfd.send(msg.encode())
    data = sockfd.recv(128).decode()
    if data == 'OK':
        while True:
            data = sockfd.recv(2048).decode()
            if data == "##":
                break
            print(data)
    else:
        print("没有查询记录")


           

