import { get, post, put, deleteJson } from '../util/axios'

const ampApi = {
    connectSign: (p) => get('/AUTO_AMP/connectSign', p),
    I: (p) => get('/AUTO_AMP/I', p),
    V: (p) => get('/AUTO_AMP/V', p),
}

export default ampApi