#从另一个主机下载文件至本地e:/share_file
#将另一个主机的分块文件整合为一个文件
import socket
import sys

f_path = 'e:/share_file'

def proma(num, sum):
    bar_len = 50
    percent = float(num) / float(sum)
    hashes = '*' * int(percent * bar_len)
    spaces = ' ' * (bar_len - len(hashes))
    sys.stdout.write(
        "\r文件正在下载中: [%s] %d%%" % (hashes + spaces, percent * 100)
    )
    sys.stdout.flush()


def download(s):
    sock6 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    hostname = socket.gethostname()  # 本机的名称
    IP = socket.gethostbyname(hostname)  # 本机的IP地址
    sock6.bind((IP, 5555))
    path = f_path + '/' + s
    s, address = sock6.recvfrom(1024)
    i = 0
    number = s.decode('utf8')
    print("接收大小：" + number)
    if number.isdigit():
        size = int(number)
        sum = size
        with open(path, 'wb') as f:
            while True:
                proma(i, sum)
                if size <= 0:
                    break
                sl = min(size, 2048)
                data, address = sock6.recvfrom(sl)
                f.write(data)
                size -= 2048
                i += sl
    else:
        print("下载失败")