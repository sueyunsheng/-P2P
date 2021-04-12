import socket
import threading
import os

# 服务器使用：
# 假定客户端连接服务器后不退出
# 服务器会传txt文件给客户端解析其他客户端的IP地址和端口
# 客户端输入指令“request”来连接到服务器，此时服务器会自动发送IP.txt文件给客户端
sock = []  # sock元组用于存储ip地址和端口
filename = 'e:/IP.txt' # 发送IP.txt文件给客户端
filepath, fname = os.path.split(filename)
shotname, extension = os.path.splitext(fname)


def file_send(address): # 发送文件
    with open(filename, 'rb') as f:
        while True:
            data = f.read(1024)
            if str(data) != "b''":
                s.sendto(data, address)
            else:
                s.sendto('end'.encode('utf-8'), address)
                break


def request_client():  # 接收客户端的ip地址和端口
    while True:
        data, address = s.recvfrom(1024)  # 设置接收的最大字节
        recv_data = data.decode()
        addr_list = list(address)
        addr_str = str(addr_list)
        with open(filename, 'r') as read:
            lines = read.readline()
        if address not in sock and recv_data == "request":
            print("连接成功")
            print("来自:" + addr_str)
            sock.append(address)
            with open(filename, 'a', encoding='utf-8') as wr:  # 写入文件
                if addr_str not in lines:
                    wr.write(addr_str + '\n')
            file_send(address)

        # 当发送数据为close时，客户端关闭套接字，服务器删除客户端的ip地址
        elif recv_data == "close":
            sock.remove(address)

        else:
            print(recv_data)
            s.sendto(recv_data.encode('utf8'), address)


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    hostname = socket.gethostname()  # 服务端的名称
    this_IP = socket.gethostbyname(hostname)  # 服务端的IP地址
    with open(filename, 'a', encoding='utf-8') as ft:  # 服务器运行前将IP.txt文件清空
        ft.truncate(0)
    print(this_IP)
    s.bind((this_IP, 9999))
    print("等待连接中...")
    t = threading.Thread(target=request_client)
    t.start()  # 创建线程响应请求
