import { mount } from '@vue/test-utils'
import AlertMap from '@/views/AlertMap.vue'

// mock axios.js como antes
vi.mock('@/axios', () => ({
  default: {
    get: vi.fn(() =>
      Promise.resolve({
        data: {
          type: 'FeatureCollection',
          features: [
            {
              type: 'Feature',
              geometry: {
                type: 'Point',
                coordinates: [-3.7038, 40.4168]
              },
              properties: {
                alert_type: 'flood',
                description: 'Mocked flood alert'
              }
            }
          ]
        }
      })
    )
  }
}))

describe('AlertMap.vue', () => {
  it('renders map container', async () => {
    // Cria um elemento real no body para o mapa
    const div = document.createElement('div')
    document.body.appendChild(div)

    const wrapper = mount(AlertMap, {
      attachTo: div // importante!
    })

    expect(wrapper.find('#map').exists()).toBe(true)
  })
})
