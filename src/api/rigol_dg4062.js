import { get, post, put, deleteJson } from '../util/axios'

const rigol_dg4062Api = {
    connect: (p) => post('/RIGOL_DG4062/connect', p),
    connectSign: (p) => get('/RIGOL_DG4062/connectSign', p),
    outputIMP: (p) => post('/RIGOL_DG4062/outputIMP', p),
    output: (p) => post('/RIGOL_DG4062/output', p),
    applySIN: (p) => post('/RIGOL_DG4062/applySIN', p),
}

export default rigol_dg4062Api