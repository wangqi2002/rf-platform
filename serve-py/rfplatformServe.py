import json
import math
import requests
from gevent.pywsgi import WSGIServer
from flask import Flask, jsonify, request
from flask_cors import CORS

from FPH_serve import FPH_serve
from RIGOL_DG4062_serve import RIGOL_DG4062_serve
from RIGOL_DS4014_serve import RIGOL_DS4014_serve
from AUTO_AMP_serve import AUTO_AMP_serve

# monkey.patch_all()
app = Flask(__name__)
app.register_blueprint(FPH_serve, url_prefix='/FPH')
app.register_blueprint(RIGOL_DG4062_serve, url_prefix='/RIGOL_DG4062')
app.register_blueprint(RIGOL_DS4014_serve, url_prefix='/RIGPL_DS4014')
app.register_blueprint(AUTO_AMP_serve, url_prefix='/AUTO_AMP')

cors = CORS(app)


@app.route('/FeatureOne', methods=["GET"])
def FeatureOne():
    inputPower = request.values.get('DG_InputPower')
    markNum = request.values.get('FPH_MarkNum')
    result = {}
    try:
        # 入射、反射功率计算
        reflectedPower = 1
        incidentPower = 1
        # 驻波比计算
        reflectionCoefficient = math.pow(10, (reflectedPower-incidentPower)/20)
        Standing_waveRatio = (1+reflectionCoefficient) / \
            (1-reflectionCoefficient)
        # 直流电压、电流、功率计算
        DcVoltage = 1
        DcCurrent = 1
        DcPower = DcVoltage*DcCurrent
        # AUTO_AMP 电流测量
        auto_amp_I = json.loads(app.test_client().get(
            'http://localhost:9090/AUTO_AMP/I').text)
        if (auto_amp_I != {}):
            auto_amp_I = auto_amp_I['value']
        result['auto_amp_I'] = auto_amp_I
        # AUTO_AMP 电压测量
        auto_amp_V = json.loads(app.test_client().get(
            'http://localhost:9090/AUTO_AMP/V').text)
        if (auto_amp_V != {}):
            auto_amp_V = auto_amp_V['value']
        result['auto_amp_V'] = auto_amp_V
        # 输出功率计算
        auto_amp_P = 1e-6 * auto_amp_I * auto_amp_V
        result['auto_amp_P'] = auto_amp_P
        # 增益计算
        gain = 10 * math.log10(auto_amp_P / 0.001)-inputPower
        result['gain'] = gain
        # 效率计算
        # 谐波读取
        params = {
            'num': markNum,
        }
        harmonicWaveList = json.loads(app.test_client().get(
            url='http://localhost:9090/FPH/calculateMARKYR', params=params).text)
    except requests.exceptions.RequestException as e:
        print(e)
    return jsonify(result)


if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 9090), app)
    http_server.serve_forever()

# 打包, 全部打包之后将该文件放在安装目录中  win-unpacked\python-serve下
# pyinstaller --uac-admin -w -F rfplatformServe.py --distpath D:\Code\Vscode\rf-platform\dist_python --hidden-import=main