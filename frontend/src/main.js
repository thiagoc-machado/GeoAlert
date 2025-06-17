import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import 'leaflet/dist/leaflet.css'
import './assets/styles.css'

import { initializeKeycloak, keycloak } from './keycloak'

initializeKeycloak().then(() => {
  store.commit('setToken', keycloak.token)

  const app = createApp(App)
  app.use(store)
  app.use(router)
  app.config.globalProperties.$keycloak = keycloak
  app.mount('#app')

  // Redirecionar manualmente após login se estiver em /login ou /
  const currentPath = window.location.pathname
  if (keycloak.authenticated && (currentPath === '/' || currentPath === '/login')) {
    router.push('/alerts-map')
  }
})