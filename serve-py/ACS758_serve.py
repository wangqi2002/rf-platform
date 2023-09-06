# coding:utf-8
# ACS758_serve.py
import time
import backoff
import serial
import serial.tools.list_ports
from threading import Thread
from flask import Blueprint, abort, request, jsonify
ACS758_serve = Blueprint('ACS758_serve', __name__)

ser = None
cnt = 0


@backoff.on_predicate(backoff.constant, jitter=None, interval=3)
def connectPoll(portV):
    global ser
    global cnt
    cnt += 1
    if (cnt < 2):
        try:
            ser = serial.Serial(port=portV,
                                baudrate=9600,
                                bytesize=serial.EIGHTBITS,
                                stopbits=serial.STOPBITS_ONE,
                                timeout=1)
            if ser.isOpen():                        # 判断串口是否成功打开
                print("打开串口成功。")
                print(ser.name)    # 输出串口号
                ser.write("AT\r\n".encode('utf-8'))
                com_input = ser.readline().decode()
                if com_input != 'OK\r\n':
                    ser = None
                cnt = 0
                return True
            else:
                ser=None
                print("打开串口失败。")
                return False
        except Exception:
            print("AUTO_AMP连接失败")
            return False
    else:
        cnt = 0
        return True

@ACS758_serve.route('/connect', methods=["POST"])
def connect():
    port = request.json.get('port')
    threadInit = Thread(target=connectPoll, args=(port,))
    threadInit.start()
    result = {'name': 'ACS758','port': port}
    return jsonify(result)


@ACS758_serve.route('/connectSign', methods=["GET"])
def connectSign():
    if ser is None:
        result = {'name': 'ACS758', 'sign': False}
    else:
        result = {'name': 'ACS758', 'sign': True}
    return jsonify(result)


@ACS758_serve.route('/I', methods=["GET"])
def getI():
    result = {}
    try:
        ser.write("AT+C\r\n".encode('utf-8'))
        com_input = ser.readline().decode()
        ser.readline()
        if com_input:   # 如果读取结果非空，则输出
            result = {'code': 1,'value': float(
                com_input[3:7]), 'unit': 'A'}
    except Exception:
        result = {'code': 0, 'value': "设备未连接"}
    return jsonify(result)


@ACS758_serve.route('/V', methods=["GET"])
def getV():
    result = {}
    try:
        ser.write("AT+V\r\n".encode('utf-8'))
        com_input = ser.readline().decode()
        ser.readline()
        if com_input:   # 如果读取结果非空，则输出
            result = {'code': 1,'value': float(com_input[3:7]), 'unit': 'V'}
    except Exception:
        result = {'code': 0, 'value': "设备未连接"}
    return jsonify(result)
