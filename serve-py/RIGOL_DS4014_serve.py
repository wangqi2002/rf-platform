# coding:utf-8
# RIGOL_DS4014_serve.py
import time
import backoff
import pyvisa as visa
from threading import Thread
from flask import Blueprint, jsonify, request
RIGOL_DS4014_serve = Blueprint('RIGOL_DS4014_serve', __name__)

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
                'TCPIP0::192.168.2.4::inst0::INSTR')
            return True
        except Exception:
            my_instrument = None
            # print("RIGOL_DS4014——连接失败")
            return False
    else:
        return True


threadInit = Thread(target=connect)
threadInit.start()


@RIGOL_DS4014_serve.route('/connectSign', methods=["GET"])
def connectSign():
    if my_instrument is None:
        result = {'name': 'RIGOL_DS4014', 'sign': False}
    else:
        result = {'name': 'RIGOL_DS4014', 'sign': True}
    return jsonify(result)
