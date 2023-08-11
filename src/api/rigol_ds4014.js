import { get, post, put, deleteJson } from '../util/axios'

const rigol_ds4014Api = {
    gcs1: (p) => get('/RIGPL_DS4014/gcs1', p),
    pcs1: (p) => post('/RIGPL_DS4014/pcs1', p),
    connectSign: (p) => get('/RIGPL_DS4014/connectSign', p),
}

export default rigol_ds4014Api