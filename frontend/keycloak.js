const keycloak = new Keycloak({
  url: 'http://localhost:8080',
  realm: 'geoalert',
  clientId: 'frontend-client'
})

const initializeKeycloak = () =>
  new Promise((resolve, reject) => {
    keycloak.init({
      onLoad: 'check-sso',
      checkLoginIframe: false,
      silentCheckSsoRedirectUri: window.location.origin + '/silent-check-sso.html'
    }).then(() => resolve(keycloak)).catch(reject)
  })

export { keycloak, initializeKeycloak }
