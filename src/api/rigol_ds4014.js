import { get, post, put, deleteJson } from '../util/axios'

const rigol_ds4014Api = {
    connect: (p) => post('/RIGPL_DS4014/connect', p),
    connectSign: (p) => get('/RIGPL_DS4014/connectSign', p),
}

export default rigol_ds4014Api