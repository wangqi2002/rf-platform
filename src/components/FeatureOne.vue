<template>
    <div class="FeatureOne">
        <div class="one">
            <div class="instrument_name">RIGOL_DG4062</div>
            <div class="pilot_box">
                <div :class="pilotModleOne"></div>
                <span class="pilot_txt suc" v-if="flagOne">已连接</span>
                <span class="pilot_txt err" v-else>未连接</span>
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
            <button class="instrument_btn" @click="handleCs">测试</button>
        </div>
    </div>
    <div class="option">
        <button class="option_btn" @click="handleOptionOne">测试</button>
    </div>
</template>
  
<script setup>
import { ref, onMounted, getCurrentInstance } from "vue"
import fphApi from "../api/fphApi"
import ampApi from "../api/ampApi"
import rigol_dg4062 from "../api/rigol_dg4062"
import rigol_ds4014 from "../api/rigol_ds4014"
import { sleep, formatter, dBmToVpp } from "../util/tool"

const { proxy } = getCurrentInstance()
const wrapCount = 1
const DG4062 = {}
const DS4014 = {}
const FPH = {}
const parameter = ref('')

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

const handleOptionOne = async () => {
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
    console.log(rigol_dg4062.output({
        sign: outputIMPPicked.value,
        state: 'ON'
    }))
}
const handleFPHSetting = () => {
    console.log('handleFPHSetting')
}
const handleCs = () => {
    console.log("cs pooling")
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
                    // console.log(res)
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
    pilotInitializeOne()
    pilotInitializeTwo()
    pilotInitializeThree()
    pilotInitializeFour()
})

</script>

<style scoped lang="scss">
.FeatureOne {
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

    .parameterInput {
        width: 70px;
        height: 25px;
        margin: 10px;
        padding: 0 10px;
        border: 1px solid black;
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
        margin-top: 10px;
        background-color: olive;
    }
}
</style>
  