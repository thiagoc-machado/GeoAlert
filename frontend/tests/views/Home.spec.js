import { mount } from '@vue/test-utils'
import Home from '@/views/Home.vue'
import { createRouter, createMemoryHistory } from 'vue-router'

const router = createRouter({
  history: createMemoryHistory(),
  routes: []
})

describe('Home.vue', () => {
  it('renders title and buttons', () => {
    const wrapper = mount(Home, {
      global: {
        plugins: [router]
      }
    })

    expect(wrapper.text()).toContain('GeoAlert')
    expect(wrapper.find('a[href="/login"]').exists()).toBe(true)
    expect(wrapper.find('a[href="/alerts-map"]').exists()).toBe(true)
    expect(wrapper.find('img').exists()).toBe(true)
  })
})
