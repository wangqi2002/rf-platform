# coding:utf-8
# AUTO_AMP_serve.py
import time
import backoff
import serial
import serial.tools.list_ports
from threading import Thread
from flask import Blueprint, abort, request, jsonify
AUTO_AMP_serve = Blueprint('AUTO_AMP_serve', __name__)

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
                if com_input == 'OK\r\n':
                    ser = None
                cnt = 0
                return True
            else:
                ser = None
                print("打开串口失败。")
                return False
        except Exception:
            # print("AUTO_AMP连接失败")
            return False
    else:
        cnt = 0
        return True

@AUTO_AMP_serve.route('/connect', methods=["POST"])
def connect():
    port = request.json.get('port')
    threadInit = Thread(target=connectPoll, args=(port,))
    threadInit.start()
    result = {'name': 'AUTO_AMP','port': port}
    return jsonify(result)


@AUTO_AMP_serve.route('/connectSign', methods=["GET"])
def connectSign():
    if ser is None:
        result = {'name': 'AUTO_AMP', 'sign': False}
    else:
        result = {'name': 'AUTO_AMP', 'sign': True}
    return jsonify(result)


@AUTO_AMP_serve.route('/I', methods=["GET"])
def getI():
    result = {}
    try:
        com_input = ser.read_until(expected=b'\n')
        com_input = com_input.decode()
        if com_input:   # 如果读取结果非空，则输出
            result = {'code': 1,'value': float(
                com_input[2:10]), 'unit': com_input[10:12].replace(' ', '')}
            if (result['unit'] == 'mA'):
                result['value'] = result['value']*1e-3
            if (result['unit'] == 'uA'):
                result['value'] = result['value']*1e-6
    except Exception:
        result = {'code': 0, 'value': "设备未连接"}
    return jsonify(result)


@AUTO_AMP_serve.route('/V', methods=["GET"])
def getV():
    result = {}
    try:
        com_input = ser.read_until(expected=b'\n')
        com_input = com_input.decode()
        result = {}
        if com_input:   # 如果读取结果非空，则输出
            result = {'code': 1,'value': float(com_input[-11:-3]), 'unit': 'V'}
    except Exception:
        result = {'code': 0, 'value': "设备未连接"}
    return jsonify(result)
