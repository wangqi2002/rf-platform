# coding:utf-8
# AUTO_AMP_serve.py
import time
import backoff
from geventwebsocket import WebSocketError
import serial
import serial.tools.list_ports
from threading import Thread
from flask import Blueprint, abort, request, jsonify
AUTO_AMP_serve = Blueprint('AUTO_AMP_serve', __name__)

ser = None
cnt = 0


@backoff.on_predicate(backoff.constant, jitter=None, interval=3)
def connect():
    global ser
    try:
        ser = serial.Serial(port="COM3",
                            baudrate=9600,
                            bytesize=serial.EIGHTBITS,
                            stopbits=serial.STOPBITS_ONE,
                            timeout=1)

        if ser.isOpen():                        # 判断串口是否成功打开
            print("打开串口成功。")
            print(ser.name)    # 输出串口号
            return True
        else:
            print("打开串口失败。")
            return False
    except Exception:
        # print("AUTO_AMP连接失败")
        return False


threadInit = Thread(target=connect)
threadInit.start()


@AUTO_AMP_serve.route('/gcs1', methods=["GET"])
def gcs1():
    result = {'name': 'AUTO_AMP_serve', 'cs': request.values.get('cs')}
    return jsonify(result)


@AUTO_AMP_serve.route('/pcs1', methods=["POST"])
def pcs1():
    result = {'name': 'AUTO_AMP_serve', 'cs': request.json.get('cs')}
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
    com_input = ser.read_until(expected=b'\n')
    com_input = com_input.decode()
    result = {}
    if com_input:   # 如果读取结果非空，则输出
        result = {'value': float(
            com_input[2:10]), 'unit': com_input[10:12].replace(' ', '')}
        if result['unit'] == 'A':
            result['value'] = result['value']*1e6
        if result['unit'] == 'mA':
            result['value'] = result['value']*1e3
    return jsonify(result)


@AUTO_AMP_serve.route('/V', methods=["GET"])
def getV():
    com_input = ser.read_until(expected=b'\n')
    com_input = com_input.decode()
    result = {}
    if com_input:   # 如果读取结果非空，则输出
        result = {'value': float(com_input[-11:-3]), }
    return jsonify(result)
