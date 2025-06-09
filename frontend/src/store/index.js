import { createStore } from 'vuex'
import axios from '../axios'

export default createStore({
  state: {
    token: localStorage.getItem('token') || null
  },
  mutations: {
    setToken(state, token) {
      state.token = token
      localStorage.setItem('token', token)
    },
    clearToken(state) {
      state.token = null
      localStorage.removeItem('token')
    }
  },
  actions: {
    async login({ commit }, credentials) {
      const response = await axios.post('/auth/login/', credentials)
      commit('setToken', response.data.access)
    },
    logout({ commit }) {
      commit('clearToken')
    }
  },
  getters: {
    isAuthenticated: state => !!state.token
  }
})
