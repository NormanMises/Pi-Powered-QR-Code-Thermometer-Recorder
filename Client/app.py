import os
import socket

from flask import Flask, request, render_template, redirect, jsonify, url_for

from DHT11 import measure
from Light import Light
from Sensor_ultrasonic import Sensor_ultrasonic
from get_ip import get_host_ip
from pin_dic import pin_dic
from videoprocessing import VideoCamera
from buzzer import buzzer
host_ip = '192.168.38.179'
my_ip = get_host_ip()
cam = VideoCamera(0)
light = Light(pin_dic['G17'], pin_dic['G16'], pin_dic['G13'])
ultrasonic = Sensor_ultrasonic(pin_dic['G18'], pin_dic['G19'])
sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
buzzer = buzzer(pin_dic['G12'])
app = Flask(__name__)


@app.route('/temperature_get', methods=['GET', 'POST'])
def temperature_get():
    if request.method == 'GET':
        print(f'{cam.id}, please get close to take the temperature.')
        dis = 0x3f3f3f3f
        while dis > 10:
            # print(dis)
            dis = ultrasonic.distance()
        print('Temperature measurement in progress...')
        temperature, _ = measure()
        print(f'Your temperature is: {temperature} C')
        if temperature > 20:
            buzzer.alert(1)
        msg = f'{cam.id}, {temperature}'
        try:
            print('Saving in progress...')
            sender.sendto(msg.encode(), (host_ip, 8081))  # 目的ip
            print('Success.')
        except:
            print('Failed to save, please scan the code again and measure the temperature.')
        return render_template('temperature_get.html', id=cam.id, temperature=temperature)
    elif request.method == 'POST':
        st = request.form.get('reboot')
        if st == 'true':
            cam.id = '-1'
            return redirect('/')


@app.route('/QR_Scan', methods=['GET', 'POST'])
def QR_Scan():
    cam.id = '-1'
    # if cam.id in cam.flag_list:
    #     return redirect('/temperature_get')
    if request.method == 'GET':
        # cam.id = -1
        return render_template('QR_Scan.html')


@app.route('/QR_check')  # 检测二维码 不显示
def check():
    cam.id = '-1'
    # print(f'QR_check {cam.id}')
    cam.get_frame()
    # print(f'QR_check after {cam.id}')
    return jsonify({'id': cam.id})


@app.route('/', methods=['GET', 'POST'])
def index():
    file_name_list = os.listdir('./static/images')
    list = [url_for('static', filename='images/' + x) for x in file_name_list]
    if request.method == 'POST':
        st = request.form.get('status')
        # print(f'{st}')
        if st == 'begin':
            cam.id = '-1'
            # print(f'redirect')
            return redirect('/QR_Scan')
    else:
        return render_template('index.html', file=list)


if __name__ == '__main__':
    try:
        # data_skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # data_skt.bind(my_ip, 8082)
        light.setColor(0x008000)
        print('socket connection is established.')

        my_ip = 'ip,' + my_ip
        sender.sendto(my_ip.encode(), (host_ip, 8081))  # 测试
        print(my_ip)
    except:
        print('Failed to establish socket connection.')
        light.setColor(0xFF0000)

    app.run(host=get_host_ip(), port=8080)
