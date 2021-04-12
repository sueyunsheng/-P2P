# 发送给服务端本地文件表
# 本地文件夹位置为 E:\share_file
# 存储文件的消息摘要和文件名，发送给服务端
import os
import random
alphabet = 'abcdefghijklmnopqrstuvwxyz!@#$%^&*()'

file_path = 'e:/share_file'
file_table = 'e:/file_table.txt'


def file_sum():  # 返回文件长度
    files = os.listdir(file_path)
    f_sum = len(files)
    return f_sum


def open_file():  # 加入文件表
    files = os.listdir(file_path)
    with open(file_table, 'w', encoding='utf8') as f:
        f.truncate(0)
        for file in files:
            if not os.path.isdir(file):
                f.write(file + '\n')


def is_ownfile(file): # 返回是否存在本地的share_file文件夹里
    with open(file_table, 'r') as f:
        for line in f.readlines():
            s = str(line).split('\n')[0]
            if file == s:
                return False
    return True


def add_to_table(file): # 加入到文件表
    with open(file_table, 'a') as f:
        f.write(file + '\n')


def file_name_create(): #其他主机的file_table文件表名称
    name = 'file_table_'
    count = 0
    while True:
        count += 1
        name += random.choice(alphabet)
        if count == 6:
            break
    name += '.txt'
    return name