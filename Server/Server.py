import socket
import sqlite3
import time

from get_ip import get_host_ip

data_ip = 0


def receive():
    my_ip = get_host_ip()
    print(my_ip)
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((my_ip, 8081))  # 本机
    print("UDP bound on port 8081...")
    while True:
        data, addr = server.recvfrom(65535)
        dat = data.decode()
        print(dat)
        data = dat.split(',')
        data = [t.strip() for t in data]
        if data[0] == 'ip':
            # data_ip = data[1]
            continue
        deposit(dat)


def deposit(msg: str):
    info = msg.split(',')
    info = [t.strip() for t in info]
    info[1] = float(info[1])
    print(info)
    cursor.execute('insert into user values (?, ?, ?)',
                   (time.strftime("%Y-%m-%d %H-%M-%S", time.localtime()), info[0], info[1]))
    print(f'{cursor.rowcount} row was inserted')
    conn.commit()


if __name__ == "__main__":
    conn = sqlite3.connect('temperatureLog.db')
    cursor = conn.cursor()
    cursor.execute('create table if not exists user (time varchar(20) primary key, id varchar(20), temperature float)')
    # data_sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        receive()
        print('22222')
    except:
        cursor.close()
        conn.close()
