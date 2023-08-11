import { get, post, put, deleteJson } from '../util/axios'

const ampApi = {
    gcs1: (p) => get('/AUTO_AMP/gcs1', p),
    pcs1: (p) => post('/AUTO_AMP/pcs1', p),
    connectSign: (p) => get('/AUTO_AMP/connectSign', p),
    I: (p) => get('/AUTO_AMP/I', p),
    V: (p) => get('/AUTO_AMP/V', p),
}

export default ampApi