// src/keycloak.js
import Keycloak from 'keycloak-js'

const keycloak = new Keycloak({
  url: 'http://localhost:8080/',
  realm: 'geoalert',
  clientId: 'frontend-client'
})

const initializeKeycloak = () =>
  new Promise((resolve, reject) => {
    keycloak.init({ onLoad: 'login-required' }).then(authenticated => {
      if (authenticated) {
        resolve(keycloak)
      } else {
        reject('Não autenticado pelo Keycloak')
      }
    }).catch(reject)
  })

export { keycloak, initializeKeycloak }
