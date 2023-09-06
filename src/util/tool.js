const pi = 3.14159265359;   // Just pi [1].
const Z_0 = 120 * pi;         // Impedance of vacum [Ohm].
const c_0 = 3E8;            // Speed of light in vacum [m/s].

// 睡眠函数
function sleep(millisecond, fun, parameters) {
    return new Promise(resolve => {
        setTimeout(() => {
            if (fun) {
                resolve(fun(parameters))
            } else {
                resolve()
            }
        }, millisecond)
    })
}

// 取有效数字
const formatter = (digit) => {
    return new Intl.NumberFormat('en-US', {
        maximumFractionDigits: digit,
    })
}

// 振幅单位转换 dbm--vpp
function dBmToVpp(amplitude) {
    let d = amplitude;
    let R = 50;
    if (amplitude === "" || amplitude == undefined) {
        d = 1;
    }
    let k1 = d / 10
    let k2 = 10 ** k1
    let w = k2 * 0.001
    let k3 = w * R
    let k4 = Math.sqrt(k3)
    let vpp = k4 * (2 * Math.sqrt(2))
    return vpp
}

export {
    sleep,
    formatter,
    dBmToVpp,
}