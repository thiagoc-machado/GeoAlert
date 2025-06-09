import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import 'leaflet/dist/leaflet.css'
import './assets/styles.css'

createApp(App)
  .use(router)
  .use(store)
  .mount('#app')