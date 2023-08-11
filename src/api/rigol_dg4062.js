import { get, post, put, deleteJson } from '../util/axios'

const rigol_dg4062Api = {
    gcs1: (p) => get('/RIGOL_DG4062/gcs1', p),
    pcs1: (p) => post('/RIGOL_DG4062/pcs1', p),
    connectSign: (p) => get('/RIGOL_DG4062/connectSign', p),
    outputIMP: (p) => post('/RIGOL_DG4062/outputIMP', p),
    output: (p) => post('/RIGOL_DG4062/output', p),
    applySIN: (p) => post('/RIGOL_DG4062/applySIN', p),
}

export default rigol_dg4062Api