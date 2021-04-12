#分块向另一个用户发送文件，首先将文件分块保存到本地e:\blocks，暂时存储文件块
# 然后创建多线程将分块文件通过udp发送给另一个用户
import os
import socket
import trans
import time
import math
# import math
import sys
file_dir = 'e:/share_file'


def file_size(file):
    listfile = os.listdir(file_dir)
    print(listfile)
    flag = False
    for l in listfile:
        if file == l.split('e:/share_file')[0]:
            flag = True
            break
    if flag:
        return os.path.getsize(file_dir + '/' + file)


def proma(num, sum):
    bar_len = 50
    percent = float(num) / float(sum)
    hashes = '*' * int(percent * bar_len)
    spaces = ' ' * (bar_len - len(hashes))
    sys.stdout.write(
        "\r文件正在上传中: [%s] %d%%" % (hashes + spaces, percent * 100)
    )
    sys.stdout.flush()


def up_file(file, address):
    size = file_size(file)
    sum = size
    iii = str(size)
    # sum = float(math.ceil(size / 2048))
    path = file_dir + '/' + file
    hostname = socket.gethostname()  # 本机的名称
    IP = socket.gethostbyname(hostname)  # 本机的IP地址
    sock5 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock5.bind((IP, 4444))
    ADDR = trans.to_pull_addr4(address)
    i = 0
    time.sleep(0.2)
    sock5.sendto(iii.encode('utf8'), ADDR)
    with open(path, 'rb') as f:
        while True:
            proma(i, sum)
            if size <= 0:
                break
            s = min(size, 2048)
            data = f.read(s)
            sock5.sendto(data, ADDR)
            size -= 2048
            i += s
    print("文件上传成功！")

    