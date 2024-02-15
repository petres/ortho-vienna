import '../assets/styles/main.scss';

// import { Tab } from 'bootstrap';

import { createApp } from 'vue'
import { router } from '@/router.js'
import { store } from '@/store.js'

import App from '@/App.vue'

const app = createApp(App)
    .use(router)
    .use(store)
    .mount('#app')
