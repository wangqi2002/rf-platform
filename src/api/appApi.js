import { get, post, put, deleteJson } from '../util/axios'

const appApi = {
    FeatureOne: (p) => get('/FeatureOne', p),
}

export default appApi