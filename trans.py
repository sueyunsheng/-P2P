import os
import socket


def to_addr(recv_str):  # 解析地址，以元组的方式返回
    recv_str = recv_str.strip('[\'')
    recv_str = recv_str.strip(']\n')
    i = recv_str.split(', ')
    i[0] = i[0].strip('\'')
    ADDR = (i[0], int(i[1]))
    return ADDR


def to_pull_addr(addr):  # 将端口转为6666，为文件表传输的端口
    addr_str = str(addr)
    #print(addr_str)
    addr_str = addr_str.strip('(\'')
    addr_str = addr_str.strip(')')
    i = addr_str.split(', ')
    i[0] = i[0].strip('\'')
    ADDR = (i[0], 6666)
    return ADDR


def to_pull_addr2(addr):  # 将端口转为6666，为文件表传输的端口
    addr_str = str(addr)
    #print(addr_str)
    addr_str = addr_str.strip('(\'')
    addr_str = addr_str.strip(')')
    i = addr_str.split(', ')
    i[0] = i[0].strip('\'')
    ADDR = (i[0], 7777)
    return ADDR


def to_pull_addr3(addr):  # 将端口转为6666，为文件表传输的端口
    addr_str = str(addr)
    #print(addr_str)
    addr_str = addr_str.strip('(\'')
    addr_str = addr_str.strip(')')
    i = addr_str.split(', ')
    i[0] = i[0].strip('\'')
    ADDR = (i[0], 4444)
    return ADDR


def to_pull_addr4(addr):  # 将端口转为6666，为文件表传输的端口
    addr_str = str(addr)
    #print(addr_str)
    addr_str = addr_str.strip('(\'')
    addr_str = addr_str.strip(')')
    i = addr_str.split(', ')
    i[0] = i[0].strip('\'')
    ADDR = (i[0], 5555)
    return ADDR

