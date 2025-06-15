import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import 'leaflet/dist/leaflet.css'
import './assets/styles.css'

import { initializeKeycloak, keycloak } from './keycloak'

initializeKeycloak()
  .then(() => {
    store.commit('setToken', keycloak.token) // Atualiza o token no Vuex

    const app = createApp(App)
    app.use(router)
    app.use(store)
    app.config.globalProperties.$keycloak = keycloak
    app.mount('#app')
  })
  .catch((err) => {
    console.error('Erro ao inicializar o Keycloak:', err)
  })
