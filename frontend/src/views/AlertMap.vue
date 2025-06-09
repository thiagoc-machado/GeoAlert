<template>
  <div class="alert-map-page">
    <!-- Barra superior -->
    <header class="top-bar">
      <span class="user-info">👤 {{ username }}</span>
      <div class="actions">
        <button class="btn secondary" @click="openProfile">View Profile</button>
        <button class="btn primary" @click="handleLogout">Logout</button>
      </div>
    </header>

    <!-- Conteúdo do mapa -->
    <div class="map-container">
      <h1>🗺️ Live Alert Map</h1>
      <p class="subtitle">View real-time geographic alerts on the map.</p>
      <div id="map" class="leaflet-map"></div>
    </div>

    <!-- Modal de perfil -->
    <div class="modal" v-if="showProfile">
      <div class="modal-content">
        <h2>User Profile</h2>

        <template v-if="editing">
          <input v-model="profile.first_name" placeholder="First name" class="form-input" />
          <input v-model="profile.last_name" placeholder="Last name" class="form-input" />
          <input v-model="profile.email" placeholder="Email" class="form-input" />
          <div class="modal-actions">
            <button class="btn secondary" @click="saveProfile">Save</button>
            <button class="btn primary" @click="editing = false">Cancel</button>
          </div>
        </template>

        <template v-else>
          <p><strong>Username:</strong> {{ profile.username }}</p>
          <p><strong>Email:</strong> {{ profile.email }}</p>
          <p><strong>Name:</strong> {{ profile.first_name }} {{ profile.last_name }}</p>
          <div class="modal-actions">
            <button class="btn secondary" @click="editing = true">Edit</button>
            <button class="btn primary" @click="showProfile = false">Close</button>
          </div>
        </template>
      </div>
    </div>

    <!-- Mapa Leaflet -->
    <div id="map" class="leaflet-map"></div>
  </div>
</template>

<script>
import L from 'leaflet'
import axios from '../axios'
import { mapState, mapActions } from 'vuex'

export default {
  name: 'AlertMap',
  data() {
    return {
      map: null,
      showProfile: false,
      editing: false,
      profile: {
        username: '',
        email: '',
        first_name: '',
        last_name: ''
      }
    }
  },
  computed: {
    ...mapState(['token']),
    username() {
      return this.profile.username || 'User'
    },
    email() {
      return this.profile.email || ''
    }
  },
  methods: {
    ...mapActions(['logout']),
    handleLogout() {
      this.logout()
      this.$router.push('/')
    },
    openProfile() {
      this.showProfile = true
      axios.get('/auth/me/').then(res => {
        this.profile = res.data
      })
    },
    saveProfile() {
      axios.put('/auth/me/', this.profile)
        .then(() => {
          this.editing = false
        })
        .catch(() => {
          alert('Error saving profile.')
        })
    }
  },
  mounted() {
    this.map = L.map('map').setView([40.4168, -3.7038], 6)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(this.map)

    axios.get('/alerts/')
      .then(res => {
        L.geoJSON(res.data, {
          onEachFeature: (feature, layer) => {
            const props = feature.properties
            layer.bindPopup(`<strong>Type:</strong> ${props.alert_type}<br><strong>Description:</strong> ${props.description}`)
          }
        }).addTo(this.map)
      })
      .catch(err => {
        console.error('Failed to load alerts:', err)
      })
  }
}
</script>

<style scoped>
.alert-map-page {
  font-family: 'Segoe UI', sans-serif;
}

/* Barra superior */
.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #2c3e50;
  color: white;
  padding: 1rem 2rem;
  border-bottom: 3px solid #1abc9c;
}

.actions button {
  margin-left: 0.5rem;
}

.user-info {
  font-size: 1rem;
  font-weight: 500;
}

/* Modal */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: #00000088;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}


.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  max-width: 400px;
  text-align: center;
}

.modal-actions {
  margin-top: 1rem;
  display: flex;
  justify-content: center;
  gap: 1rem;
}

/* Mapa */
.map-container {
  padding: 2rem;
  text-align: center;
}

.leaflet-map {
  height: 500px;
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}
</style>
