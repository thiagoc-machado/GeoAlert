import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'
import Login from '../views/Login.vue'
import AlertMap from '../views/AlertMap.vue'
import Home from '../views/Home.vue'
import { keycloak } from '../keycloak'

const routes = [
  { path: '/', component: Home },
  { path: '/login', component: Login },
  {
    path: '/alerts-map',
    component: AlertMap,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !keycloak.authenticated) {
    keycloak.login({ redirectUri: window.location.origin + to.fullPath })
  } else {
    next()
  }
})

export default router
