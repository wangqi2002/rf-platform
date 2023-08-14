# coding:utf-8
# RIGOL_DG4062_serve.py
import time
import backoff
import pyvisa as visa
from threading import Thread
from flask import Blueprint, jsonify, request
RIGOL_DG4062_serve = Blueprint('RIGOL_DG4062_serve', __name__)

rm = visa.ResourceManager()
my_instrument = None
cnt = 0


@backoff.on_predicate(backoff.constant, jitter=None, interval=1)
def connect():
    global my_instrument
    global cnt
    cnt += 1
    if (cnt < 20):
        try:
            my_instrument = rm.open_resource(
                'TCPIP0::192.168.2.3::inst0::INSTR')
            return True
        except Exception:
            my_instrument = None
            # print("RIGOL_DG4062——连接失败")
            return False
    else:
        return True


threadInit = Thread(target=connect)
threadInit.start()


@RIGOL_DG4062_serve.route('/connectSign', methods=["GET"])
def connectSign():
    if (my_instrument is None):
        result = {'name': 'RIGOL_DG4062', 'sign': False}
    else:
        result = {'name': 'RIGOL_DG4062', 'sign': True}
    return jsonify(result)


@RIGOL_DG4062_serve.route('/outputIMP', methods=["POST"])
def outputIMP():
    sign = request.json.get('sign')
    i = request.json.get('impedance')
    command = ":OUTPut{0}:IMPedance {1}".format(sign, i)
    try:
        my_instrument.write(command)
        result = {'code': '1', 'value': "设置阻抗命令收到"}
    except Exception:
        result = {'code': '0', 'value': "设备未连接"}
    return jsonify(result)


@RIGOL_DG4062_serve.route('/output', methods=["POST"])
def output():
    sign = request.json.get('sign')
    state = request.json.get('state')
    command = ":OUTPut{0} {1}".format(sign, state)
    try:
        my_instrument.write(command)
        result = {'code': '1', 'value': "输出命令收到"}
    except Exception:
        result = {'code': '0', 'value': "设备未连接"}
    return jsonify(result)


@RIGOL_DG4062_serve.route('/applySIN', methods=["POST"])
def applySIN():
    f = request.json.get('frequency')
    a = request.json.get('amplitude')
    s = request.json.get('skew')
    p = request.json.get('phase')
    command = ":APPLy:SINusoid {0},{1},{2},{3}".format(f, a, s, p)
    try:
        my_instrument.write(command)
        time.sleep(0.1)
        value = my_instrument.query(":APPLy?")
        if ("SINusoid" in value):
            result = {'code': '1', 'value': "设置正弦波成功"}
        else:
            result = {'code': '0', 'value': "设置正弦波失败"}
    except Exception:
        result = {'code': '0', 'value': "设备未连接"}

    return jsonify(result)
