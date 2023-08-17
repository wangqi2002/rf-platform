<template>
    <div class="Feature">
        <div class="Feature_one">
            <div class="one">
                <div class="instrument_name">RIGOL_DG4062</div>
                <div class="pilot_box">
                    <div :class="pilotModleOne"></div>
                    <span class="pilot_txt suc" v-if="flagOne">已连接</span>
                    <span class="pilot_txt err" v-else>未连接</span>
                </div>
                <div>
                    资源名称：<input class="parameterInput" v-model="DGVisaValue" />
                    <button class="con_btn" @click="handleDGConnect">连接</button>
                </div>
                <div>
                    输出阻抗：<input class="parameterInput" type="number" v-model="outputIMPValue" />
                </div>
                <div>
                    起始频率：<input class="parameterInput" type="number" v-model="frequencySTAValue" />MHz
                </div>
                <div>
                    终止频率：<input class="parameterInput" type="number" v-model="frequencyENDValue" />MHz
                </div>
                <div>
                    频率步长：<input class="parameterInput" type="number" v-model="frequencyStepValue" />MHz
                </div>
                <div>
                    起始功率：<input class="parameterInput" type="number" v-model="amplitudeSTAValue" />dBm
                </div>
                <div>
                    终止功率：<input class="parameterInput" type="number" v-model="amplitudeENDValue" />dBm
                </div>
                <div>
                    功率步长：<input class="parameterInput" type="number" v-model="amplitudeStepValue" />dBm
                </div>
                <div>
                    DC偏移：<input class="parameterInput" type="number" v-model="skewValue" />
                </div>
                <div>
                    起始相位：<input class="parameterInput" type="number" v-model="phaseValue" />
                </div>
                <div>
                    输出接口：
                    <input type="radio" id="output1" value="1" v-model="outputIMPPicked">
                    <label for="output1" style="margin-right:10px">OUTPUT1</label>
                    <input type="radio" id="output2" value="2" v-model="outputIMPPicked">
                    <label for="output2">OUTPUT2</label>
                </div>
                <button class="instrument_btn" @click="handleDGSetting">设置</button>
            </div>
            <div class="two">
                <div class="instrument_name">RIGOL_DS4014</div>
                <div class="pilot_box">
                    <div :class="pilotModleTwo"></div>
                    <span class="pilot_txt suc" v-if="flagTwo">已连接</span>
                    <span class="pilot_txt err" v-else>未连接</span>
                </div>
                <div>
                    资源名称：<input class="parameterInput" v-model="DSVisaValue" />
                    <button class="con_btn" @click="handleDSConnect">连接</button>
                </div>
                <div>
                    参数：<input class="parameterInput" type="number" v-model="parameter" />
                </div>
                <div>
                    参数：<input class="parameterInput" type="number" v-model="parameter" />
                </div>
                <div>
                    参数：<input class="parameterInput" type="number" v-model="parameter" />
                </div>
                <div>
                    参数：<input class="parameterInput" type="number" v-model="parameter" />
                </div>
            </div>
            <div class="three">
                <div class="instrument_name">FPH</div>
                <div class="pilot_box">
                    <div :class="pilotModleThree"></div>
                    <span class="pilot_txt suc" v-if="flagThree">已连接</span>
                    <span class="pilot_txt err" v-else>未连接</span>
                </div>
                <div>
                    资源名称：<input class="parameterInput" v-model="FPHVisaValue" />
                    <button class="con_btn" @click="handleFPHConnect">连接</button>
                </div>
                <div>
                    中心频率：<input class="parameterInput" type="number" v-model="freqCenterValue" />
                </div>
                <div>
                    起始频率：<input class="parameterInput" type="number" v-model="freqStartValue" />
                </div>
                <div>
                    终止频率：<input class="parameterInput" type="number" v-model="freqEndValue" />
                </div>
                <div>
                    谐波次数：<input class="parameterInput" type="number" v-model="markNumValue" />
                </div>
                <button class="instrument_btn" @click="handleFPHSetting">设置</button>
            </div>
            <div class="four">
                <div class="instrument_name">AUTO_AMP</div>
                <div class="pilot_box">
                    <div :class="pilotModleFour"></div>
                    <span class="pilot_txt suc" v-if="flagFour">已连接</span>
                    <span class="pilot_txt err" v-else>未连接</span>
                </div>
                <button class="instrument_btn" style="background-color: #daffe0" @click="handleAMPConnect">连接</button>
                <br />
                <button class="instrument_btn" @click="handleAMPivw">GET IVW</button>
            </div>
        </div>
        <div class="option">
            <button class="option_btn" @click="handleOptionOne">开始</button>
            <button class="option_btn" @click="handleDialog">Open Dialog</button>
        </div>
        <el-dialog class="result_box" v-model="dialogVisible" title="返回结果" draggable>
            <span>
                <DataTable></DataTable>
            </span>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="handleSave">Save</el-button>
                    <el-button @click="handleEmit">Emit</el-button>
                    <el-button type="primary" @click="handleClose">Close</el-button>
                </span>
            </template>
        </el-dialog>
    </div>
</template>
  
<script setup>
import DataTable from '../components/DataTable.vue'
import { ref, onMounted, getCurrentInstance } from "vue"
import fphApi from "../api/fphApi"
import ampApi from "../api/ampApi"
import rigol_dg4062 from "../api/rigol_dg4062"
import rigol_ds4014 from "../api/rigol_ds4014"
import { sleep, formatter, dBmToVpp } from "../util/tool"
import emitter from "../util/mittBus.js"

const { proxy } = getCurrentInstance()
const wrapCount = 2
const DG4062 = {}
const DS4014 = {}
const FPH = {}
const parameter = ref('')

const dialogVisible = ref(false)

const DGVisaValue = ref('TCPIP0::192.168.2.15::inst0::INSTR')
const DSVisaValue = ref('')
const FPHVisaValue = ref('')

const pilotModleOne = ref('pilot_err')
const flagOne = ref(false)
const outputIMPValue = ref('')
const frequencySTAValue = ref('')
const frequencyENDValue = ref('')
const frequencyStepValue = ref(1)
const amplitudeSTAValue = ref(40)
const amplitudeENDValue = ref('')
const amplitudeStepValue = ref(0.1)
const skewValue = ref(0)
const phaseValue = ref(0)
const outputIMPPicked = ref([])

const pilotModleTwo = ref('pilot_err')
const flagTwo = ref(false)

const pilotModleThree = ref('pilot_err')
const flagThree = ref(false)
const freqCenterValue = ref()
const freqStartValue = ref()
const freqEndValue = ref()
const markNumValue = ref(3)

const pilotModleFour = ref('pilot_err')
const flagFour = ref(false)

const handleDGConnect = () => {
    console.log("handleDGConnect")
    console.log(rigol_dg4062.connect({ resource: DGVisaValue.value }))
    pilotInitializeOne()
}
const handleDSConnect = () => {
    console.log("handleDSConnect")
    pilotInitializeTwo()
}
const handleFPHConnect = () => {
    console.log("handleFPHConnect")
    pilotInitializeThree()
}
const handleAMPConnect = () => {
    console.log("handleAMPConnect")
    console.log(ampApi.connect())
    pilotInitializeFour()
}
const handleDialog = () => {
    dialogVisible.value = true
    getTableHeader()
}
const handleSave = () => {
    emitter.emit('featureOneSave')
}
const handleEmit = () => {
    emitter.emit('featureOneResult', {
        freq: 123,
        inputPower: 345,
        incidentPower: 567,
        reflectedPower: 789
    })
}
const handleClose = () => {
    ElMessageBox.confirm(
        'Has the data been saved?',
        {
            confirmButtonText: 'Yes',
            cancelButtonText: 'No',
            type: 'warning',
        }
    )
        .then(() => {
            dialogVisible.value = false
            emitter.emit("clearHeader")
        })
        .catch(() => {
            console.log('取消')
        })
}
const handleOptionOne = async () => {
    dialogVisible.value = true
    console.log('handleOptionOne', DG4062)
    for (let i = DG4062.startFREQ; i <= DG4062.endFREQ; i += DG4062.stepFREQ) {
        for (let j = DG4062.startAMPL; j <= DG4062.endAMPL; j += DG4062.stepAMPL) {
            console.log(i, Number(formatter(3).format(j)))
            let sign = await sleep(1000, rigol_dg4062.applySIN, {
                frequency: i,
                amplitude: Number(formatter(3).format(j)),
                skew: DG4062.skew,
                phase: DG4062.phase
            })
            console.log(sign)
            emitter.emit('featureOneResult', sign)
            // if (!Number(sign.code)) {
            //     break;
            // }
        }
    }
}
const handleDGSetting = () => {
    DG4062.startFREQ = frequencySTAValue.value
    DG4062.endFREQ = frequencyENDValue.value
    DG4062.stepFREQ = frequencyStepValue.value
    DG4062.startAMPL = amplitudeSTAValue.value
    DG4062.endAMPL = amplitudeENDValue.value
    DG4062.stepAMPL = amplitudeStepValue.value
    DG4062.skew = skewValue.value
    DG4062.phase = phaseValue.value
    console.log(rigol_dg4062.outputIMP({
        sign: outputIMPPicked.value,
        impedance: outputIMPValue.value
    }))
    // console.log(rigol_dg4062.output({
    //     sign: outputIMPPicked.value,
    //     state: 'ON'
    // }))
}
const handleFPHSetting = () => {
    console.log('handleFPHSetting')
}
const handleAMPivw = () => {
    console.log("pooling")
    ampApi.I()
        .then((res) => {
            console.log(res)
        })
        .catch((err) => {
            console.log(err)
        })
    ampApi.V()
        .then((res) => {
            console.log(res)
        })
        .catch((err) => {
            console.log(err)
        })
}

const pilotInitializeOne = () => {
    let timer = null
    let count = 0
    timer = setInterval(() => {
        setTimeout(() => {
            rigol_dg4062.connectSign()
                .then((res) => {
                    if (res.sign) {
                        clearInterval(timer)
                        pilotModleOne.value = 'pilot_suc'
                        flagOne.value = true
                    }
                    if (count > wrapCount) {
                        clearInterval(timer)
                    }
                })
                .catch((err) => {
                    if (count > wrapCount) {
                        clearInterval(timer)
                    }
                    console.log(err)
                })
        }, 0)
        count++
    }, 5000)
}
const pilotInitializeTwo = () => {
    let timer = null
    let count = 0
    timer = setInterval(() => {
        setTimeout(() => {
            rigol_ds4014.connectSign()
                .then((res) => {
                    // console.log(res)
                    if (res.sign) {
                        clearInterval(timer)
                        pilotModleTwo.value = 'pilot_suc'
                        flagTwo.value = true
                    }
                    if (count > wrapCount) {
                        clearInterval(timer)
                    }
                })
                .catch((err) => {
                    if (count > wrapCount) {
                        clearInterval(timer)
                    }
                    console.log(err)
                })
        }, 0)
        count++
    }, 5000)
}
const pilotInitializeThree = () => {
    let timer = null
    let count = 0
    timer = setInterval(() => {
        setTimeout(() => {
            fphApi.connectSign()
                .then((res) => {
                    // console.log(res)
                    if (res.sign) {
                        clearInterval(timer)
                        pilotModleThree.value = 'pilot_suc'
                        flagThree.value = true
                    }
                    if (count > wrapCount) {
                        clearInterval(timer)
                    }
                })
                .catch((err) => {
                    if (count > wrapCount) {
                        clearInterval(timer)
                    }
                    console.log(err)
                })
        }, 0)
        count++
    }, 5000)
}
const pilotInitializeFour = () => {
    let timer = null
    let count = 0
    timer = setInterval(() => {
        setTimeout(() => {
            ampApi.connectSign()
                .then((res) => {
                    // console.log(res)
                    if (res.sign) {
                        clearInterval(timer)
                        pilotModleFour.value = 'pilot_suc'
                        flagFour.value = true
                    }
                    if (count > wrapCount) {
                        clearInterval(timer)
                    }
                })
                .catch((err) => {
                    if (count > wrapCount) {
                        clearInterval(timer)
                    }
                    console.log(err)
                })
        }, 0)
        count++
    }, 5000)
}

onMounted(() => {
    // pilotInitializeOne()
    // pilotInitializeTwo()
    // pilotInitializeThree()
    // pilotInitializeFour()
})

// 内部调用
const getTableHeader = () => {
    let tableHeader = []
    if (flagOne.value) {
        let propertyList = [{
            prop: "freq",
            label: "频率"
        },
        {
            prop: "inputPower",
            label: "输入功率"
        },]
        tableHeader.push.apply(tableHeader, propertyList)
    }
    if (flagTwo.value) {
        let propertyList = [{
            prop: "incidentPower",
            label: "入射功率"
        },
        {
            prop: "reflectedPower",
            label: "反射功率"
        },
        {
            prop: "inputSWR",
            label: "输入驻波比"
        }]
        tableHeader.push.apply(tableHeader, propertyList)
    }
    if (flagThree.value) {
        let propertyList = [{
            prop: "directI",
            label: "直流电流"
        },
        {
            prop: "directV",
            label: "直流电压"
        },
        {
            prop: "directP",
            label: "直流功率"
        },
        {
            prop: "outputP",
            label: "输出功率"
        }]
        tableHeader.push.apply(tableHeader, propertyList)
    }
    if (flagFour.value) {
        let propertyList = [{
            prop: "fundamentalWave",
            label: "基波"
        },
        {
            prop: "secondHarmonic",
            label: "二次谐波"
        },
        {
            prop: "thirdHarmonic",
            label: "三次谐波"
        },
        {
            prop: "harmonicComponent",
            label: "谐波分量"
        }]
        tableHeader.push.apply(tableHeader, propertyList)
    }
    if (flagTwo.value && flagThree.value) {
        let propertyList = [{
            prop: "gain",
            label: "增益"
        },
        {
            prop: "efficiency",
            label: "效率"
        }]
        tableHeader.push.apply(tableHeader, propertyList)
    }
    setTimeout(() => {
        emitter.emit("setHeader", tableHeader)
    }, 300)
}
</script>

<style lang="scss">
.Feature {
    .Feature_one {
        width: 100%;
        height: 100%;
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        grid-template-rows: 500px;
        gap: 10px;

        .one {
            background-color: aliceblue;
        }

        .two {
            background-color: darkcyan;
        }

        .three {
            background-color: sandybrown;
        }

        .four {
            background-color: lavenderblush;
        }


        .instrument_name {
            width: 100%;
            margin-top: 10px;
            font-size: 18px;
        }

        .con_btn {
            border: 1px solid #a1a1a1;
            border-radius: 5px;
            background-color: #daffe0;
        }

        .parameterInput {
            width: 70px;
            height: 25px;
            margin: 10px;
            padding: 0 10px;
            border: 1px solid #858585;
            border-radius: 5px;
        }

        .instrument_btn {
            width: 100px;
            height: 25px;
            border: none;
            border-radius: 5px;
            margin-top: 10px;
            background-color: rosybrown;
        }

        .pilot_box {
            width: 100%;
            margin: 10px auto;
            height: 30px;

            .pilot_suc {
                width: 20px;
                height: 20px;
                border-radius: 50%;
                display: inline-block;
                vertical-align: middle;
                margin-right: 12px;
                background-color: greenyellow;
                box-shadow: 0 0 3px greenyellow,
                    0 0 6px greenyellow,
                    0 0 9px greenyellow;
            }

            .pilot_err {
                width: 20px;
                height: 20px;
                border-radius: 50%;
                display: inline-block;
                vertical-align: middle;
                margin-right: 12px;
                background-color: red;
                box-shadow: 0 0 3px red,
                    0 0 6px red,
                    0 0 9px red;
            }

            .pilot_txt {
                font-size: 16px;
                vertical-align: middle;
            }
        }
    }

    .option {
        .option_btn {
            width: 100px;
            height: 25px;
            border: none;
            border-radius: 5px;
            margin: 0 15px;
            margin-top: 10px;
            background-color: olive;
        }
    }

    .result_box {
        width: 80vw;
        height: 80vh;
        margin: auto;
        margin-top: 50px;
        text-align: left;

        .el-dialog__header {
            padding: 10px;
        }

        .el-dialog__body {
            height: calc(80vh - 125px);
            padding: 15px 10px;
        }

        .el-dialog__footer {
            padding: 10px;
        }
    }
}
</style>
  