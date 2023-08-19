import { get, post, put, deleteJson } from '../util/axios'

const acsApi = {
    connect: (p) => post('/ACS758/connect', p),
    connectSign: (p) => get('/ACS758/connectSign', p),
    I: (p) => get('/ACS758/I', p),
    V: (p) => get('/ACS758/V', p),
}

export default acsApi