import { mount } from '@vue/test-utils'
import Login from '@/views/Login.vue'
import { createStore } from 'vuex'
import { createRouter, createMemoryHistory } from 'vue-router'

const store = createStore({
  actions: {
    login: vi.fn(() => Promise.resolve())
  }
})

const router = createRouter({
  history: createMemoryHistory(),
  routes: []
})

describe('Login.vue', () => {
  it('renders the login form', () => {
    const wrapper = mount(Login, {
      global: {
        plugins: [store, router]
      }
    })

    expect(wrapper.find('input[placeholder="Username"]').exists()).toBe(true)
    expect(wrapper.find('input[placeholder="Password"]').exists()).toBe(true)
    expect(wrapper.find('button').text().toLowerCase()).toContain('login')
  })
})
