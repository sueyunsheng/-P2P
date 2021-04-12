import file_table
import trans
import up_file
import download_file
import socket
import threading
import time
import os

filename = 'IP.txt'
hostname = socket.gethostname()  # 本机的名称
this_IP = socket.gethostbyname(hostname)  # 本机的IP地址
sock_arr = []
f_arr = []
file_table_name = 'e:/file_table.txt'
file_name = 'ar_file_table.txt'
lose_file = []
# IP_1 = ('192.168.43.40', 7777)
# IP_2 = ('192.168.43.105', 6666)


def clear_file_table():
    with open(file_name, 'a', encoding='utf8') as f:
        f.truncate(0)
    lose_file.clear()


def check():
    print('正在检查文件...')
    with open(file_name, 'r', encoding='utf8') as f:
        with open(file_table.file_table, 'r', encoding='utf8') as f2:
            for line1 in f.readlines():
                s1 = line1.split('\n')[0]
                # print(s1)
                for line2 in f2.readlines():
                    s2 = line2.split('\n')[0]
                    # print(s2)
                    if s1 != s2:
                        lose_file.append(s1)
    print('文件检查成功')


def recv_table(): # 接收其他主机传入的文件表
    try:
        sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock2.bind((this_IP, 6666))
        clear_file_table()
        print("正在写入文件中...")
        with open(file_name, 'wb') as f:
            print("写入文件表中...")
            data, address = sock2.recvfrom(2048)
            print('接收数据...')
            f.write(data)
            print(data.decode('utf8'))
        print("文件表接收成功")
        check()
        print(lose_file)
        ADDR = trans.to_pull_addr3(address)
        if not lose_file:
            sock2.sendto('over'.encode('utf8'), ADDR)
        else:
            for s in lose_file:
                print("发送缺失文件")
                sock2.sendto(str(s).encode('utf8'), ADDR)
                print("准备下载文件: " + str(s))
                print("now loading")
                download_file.download(s)
            sock2.sendto('over'.encode('utf8'), ADDR)
        clear_file_table()
    except IOError as reason:
        print("文件表接收失败" + str(reason))
    finally:
        sock2.close()


def send_recv(address): # 发送给其他主机文件表
    file_table.open_file()
    sock3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock3.bind((this_IP, 7777))
    lt = os.path.getsize(file_table.file_table)
    with open(file_table_name, 'rb') as f:
        data = f.read(lt)
        sock3.sendto(data, address)
        print("文件表发送成功！")
    sock3.close()


def recv_pull(): # 发送给其他主机文件表
    while True:
        sock3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock3.bind((this_IP, 7777))
        data, address = sock3.recvfrom(1024)
        print("...")
        if data.decode('utf-8') == "pull":
            sock3.close()
            print("receive pull from" + str(address))
            print("now loading...")
            print("send file_table to " + str(address))
            send_recv(address)
            print("开始接收缺失文件...")
            while True:
                sock5 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock5.bind((this_IP, 4444))
                data, address = sock5.recvfrom(1024)
                print(data.decode('utf8'))
                if data.decode('utf8') == "over":
                    sock5.close()
                    break

                elif str(data) != "b''":
                    print(data.decode('utf8'))
                    # time.sleep(0.1)
                    sock5.close()
                    up_file.up_file(data.decode('utf8'), address)
                else:
                    continue
        sock3.close()


def pull(): # 发送pull指令，从其他主机获取文件表
    while True:
        for addr in sock_arr:
            sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock2.bind((this_IP, 6666))
            addr2 = trans.to_pull_addr2(addr)
            print("ready to send pull to" + str(addr2))
            sock2.sendto('pull'.encode('utf-8'), addr2)
            print("succeed send pull to " + str(addr2))
            sock2.close()
            # time.sleep(1)
            recv_table()
            time.sleep(2)


def pull_to_addr(): # 创建线程，一个发送pull，一个接收
    # th_1 = threading.Thread(target=recv_pull)
    th_2 = threading.Timer(1, pull)
    # th_1.start()
    th_2.start()
    # th_1.join(3)
    th_2.join(3)


def add_addr():  # 从其他客户端获得的消息
    # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # mutex1.acquire()
    try:
        # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # sock.bind((this_IP, 8888))
        while True:
            data, address = sock.recvfrom(1024)
            if data.decode('utf-8') == "hello":
                sock.sendto('ok'.encode('utf8'), address)
                print("成功连接到:"+str(address))
                if address not in sock_arr:
                    sock_arr.append(address)
            print("当前连接的主机有：" + str(sock_arr))
            #print(sock_arr)
            #每隔2秒进行监听
    finally:
        sock.close()


def parse_addr():  # 将IP.txt变为sock列表存储
    with open(filename, 'r') as f:
        for line in f:
            tmp = trans.to_addr(line)
            if tmp != this_sock:
                sock_arr.append(tmp)


def send_helo(): #向其他IP地址发送hello
    # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # sock.bind((this_IP, 8888))
    if len(sock_arr) != 0:
        for addr in sock_arr:
            sock.sendto("hello".encode('utf8'), addr)
            time.sleep(0.1)
            data, address = sock.recvfrom(1024)
            if data.decode('utf8') == "ok":
                print("成功连接到"+str(address))
    # sock.close()

def recv_addr():  # 接受从tracker得到的IP.txt
    mutex1.acquire()
    try: # 接受IP.txt
        # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # sock.bind((this_IP, 8888))
        with open(filename, 'wb') as f:
            while True:
                data, address = sock.recvfrom(1024)
                if str(data) != "b'end'":
                    f.write(data)
                else:
                    break
        # sock.close()
        parse_addr() #添加到IP表
        send_helo() #向其他IP发送Hello
        add_addr() #循环监听其他新加入的IP
    finally:
        mutex1.release()


if __name__ == "__main__":
    with open(filename, 'a', encoding='utf-8') as ft:  # 服务器运行前将IP.txt文件清空
        ft.truncate(0)
    file_table.open_file()
    mutex1 = threading.Lock()
    mutex2 = threading.Lock()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((this_IP, 8888))  # 客户端绑定的端口为8888
    this_sock = sock.getsockname()
    sock.sendto('request'.encode('utf-8'), ('192.168.43.246', 9999))
    t1 = threading.Thread(target=recv_addr)
    t2 = threading.Timer(5, pull_to_addr)
    t1.start()
    t2.start()
    t1.join(5)
    t2.join(5)
