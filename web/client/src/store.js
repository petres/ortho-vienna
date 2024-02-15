import { createStore } from 'vuex'

import axios from 'axios';

// import * as api from '@/shared/api.js'

const store = createStore({
    state: () => ({
        models: []
    }),
    getters: {
        initialized (state) {
            return true
        }
    },
    mutations: {
        init(state) {
            axios.get('/api/inf/models')
                .then(function (response) {
                    state.models = response.data.models
                })
        }
    }
})


export {
    store
}