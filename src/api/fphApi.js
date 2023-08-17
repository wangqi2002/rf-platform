import { get, post, put, deleteJson } from '../util/axios'

const fphApi = {
    connect: (p) => post('/FPH/connect', p),
    connectSign: (p) => get('/FPH/connectSign', p),
    calculateMARKYR: (p) => get('/FPH/calculateMARKYR', p),
    frequencyCENT: (p) => post('/FPH/frequencyCENT', p),
    frequencyCENTStep: (p) => post('/FPH/frequencyCENTStep', p),
    frequencySPAN: (p) => post('/FPH/frequencySPAN', p),
    frequencyRANGE: (p) => post('/FPH/frequencyRANGE', p),
    calculateMARKXW: (p) => post('/FPH/calculateMARKXW', p),
}

export default fphApi