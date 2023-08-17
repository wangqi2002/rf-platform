# coding:utf-8
# FPH_serve.py
import time
import backoff
import pyvisa as visa
from threading import Thread
from flask import Blueprint, request, jsonify
FPH_serve = Blueprint('FPH_serve', __name__)

rm = visa.ResourceManager()
my_instrument = None
cnt = 0


@backoff.on_predicate(backoff.constant, jitter=None, interval=1)
def connectPoll(url):
    global my_instrument
    global cnt
    cnt += 1
    if (cnt < 5):
        try:
            my_instrument = rm.open_resource(url)
            # print(my_instrument.query("*IDN?"))
            return True
        except Exception:
            my_instrument = None
            # print("FPH——连接失败")
            return False
    else:
        return True

@FPH_serve.route('/connect', methods=["POST"])
def connect():
    resourceName = request.json.get('resource')
    threadInit = Thread(target=connectPoll, args=(resourceName,))
    threadInit.start()
    result = {'name': 'FPH', 'resource': resourceName}
    return jsonify(result)


@FPH_serve.route('/connectSign', methods=["GET"])
def connectSign():
    if (my_instrument is None):
        result = {'name': 'FPH', 'sign': False}
    else:
        result = {'name': 'FPH', 'sign': True}
    return jsonify(result)


@FPH_serve.route('/frequencyCENT', methods=["POST"])
def frequencyCENT():
    cent = request.json.get('center')
    command = "FREQ:CENT {0}".format(cent)
    try:
        my_instrument.write(command)
        result = {'code': '1', 'value': "设置中心频率命令收到"}
    except Exception:
        result = {'code': '0', 'value': "设备未连接"}
    return jsonify(result)


@FPH_serve.route('/frequencyCENTStep', methods=["POST"])
def frequencyCENTStep():
    step = request.json.get('step')
    command = "FREQ:CENT:STEP {0}".format(step)
    try:
        my_instrument.write(command)
        result = {'code': '1', 'value': "设置中心频率步长命令收到"}
    except Exception:
        result = {'code': '0', 'value': "设备未连接"}
    return jsonify(result)


@FPH_serve.route('/frequencySPAN', methods=["POST"])
def frequencySPAN():
    span = request.json.get('span')
    command = "FREQ:SPAN {0}".format(span)
    try:
        my_instrument.write(command)
        result = {'code': '1', 'value': "设置频率范围命令收到"}
    except Exception:
        result = {'code': '0', 'value': "设备未连接"}
    return jsonify(result)


@FPH_serve.route('/frequencyRANGE', methods=["POST"])
def frequencyRANGE():
    start = request.json.get('start')
    end = request.json.get('start')
    command = "SENSe:FREQ:STAR {0};STOP {1}".format(start, end)
    try:
        my_instrument.write(command)
        result = {'code': '1', 'value': "设置测量频率范围命令收到"}
    except Exception:
        result = {'code': '0', 'value': "设备未连接"}
    return jsonify(result)


@FPH_serve.route('/calculateMARKXW', methods=["POST"])
def calculateMARKXW():
    num = request.json.get('num')
    start = request.json.get('start')
    step = request.json.get('step')
    try:
        for i in range(1, num):
            command = "CALC:MARK{0}:X {1}".format(i, start+step*(i-1))
            my_instrument.write(command)
        result = {'code': '1', 'value': "设置标记定位命令收到"}
    except Exception:
        result = {'code': '0', 'value': "设备未连接"}
    return jsonify(result)


@FPH_serve.route('/calculateMARKYR', methods=["GET"])
def calculateMARKYR():
    # CALC:MARK2:Y?
    num = request.values.get('num')
    command = "CALC:MARK{0}:Y?".format(num)
    result = []
    # todo 检查是否有单位
    try:
        for i in range(1, num):
            command = "CALC:MARK{0}:Y?".format(i)
            obj = {'id': i, 'value': float(my_instrument.query(command))}
            result.append(obj)
    except Exception:
        result.append({'code': '0', 'value': "设备未连接"})
    return jsonify(result)
