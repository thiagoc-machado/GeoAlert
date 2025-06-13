<template>
    <div class="alert-map-page">
        <!-- Barra superior -->
        <header class="top-bar">
            <span class="user-info">👤 {{ username }}</span>
            <div class="actions">
                <button class="btn secondary" @click="openProfile">
                    View Profile
                </button>
                <button class="btn primary" @click="handleLogout">
                    Logout
                </button>
            </div>
        </header>

        <!-- Conteúdo do mapa -->
        <div class="map-container">
            <h1>🗺️ Live Alert Map</h1>
            <p class="subtitle">View real-time geographic alerts on the map.</p>

            <!-- Filtros -->
            <div class="filters">
                <input
                    v-model="searchCity"
                    placeholder="Search city..."
                    class="form-input"
                    @keyup.enter="searchByCity"
                />
                <select v-model="filterType" class="form-input">
                    <option value="">All Types</option>
                    <option value="flood">Flood</option>
                    <option value="fire">Fire</option>
                    <option value="construction">Construction</option>
                </select>
                <input
                    type="date"
                    v-model="filterStartDate"
                    class="form-input"
                />
                <input type="date" v-model="filterEndDate" class="form-input" />
                <input
                    type="number"
                    v-model.number="filterRadius"
                    class="form-input"
                    placeholder="Radius (km)"
                />
                <button class="btn primary" @click="loadAlerts">
                    Apply Filters
                </button>
            </div>

            <div id="map" class="leaflet-map"></div>
        </div>

        <!-- Modal de perfil -->
        <div class="modal" v-if="showProfile">
            <div class="modal-content">
                <h2>User Profile</h2>

                <template v-if="editing">
                    <input
                        v-model="profile.first_name"
                        placeholder="First name"
                        class="form-input"
                    />
                    <input
                        v-model="profile.last_name"
                        placeholder="Last name"
                        class="form-input"
                    />
                    <input
                        v-model="profile.email"
                        placeholder="Email"
                        class="form-input"
                    />
                    <div class="modal-actions">
                        <button class="btn secondary" @click="saveProfile">
                            Save
                        </button>
                        <button class="btn primary" @click="editing = false">
                            Cancel
                        </button>
                    </div>
                </template>

                <template v-else>
                    <p><strong>Username:</strong> {{ profile.username }}</p>
                    <p><strong>Email:</strong> {{ profile.email }}</p>
                    <p>
                        <strong>Name:</strong> {{ profile.first_name }}
                        {{ profile.last_name }}
                    </p>
                    <div class="modal-actions">
                        <button class="btn secondary" @click="editing = true">
                            Edit
                        </button>
                        <button
                            class="btn primary"
                            @click="showProfile = false"
                        >
                            Close
                        </button>
                    </div>
                </template>
            </div>
        </div>
    </div>
</template>

<script>
    import L from "leaflet";
    import axios from "../axios";
    import { mapState, mapActions } from "vuex";
    import wellknown from 'wellknown'

    export default {
        name: "AlertMap",
        data() {
            return {
                alertLayer: null,
                map: null,
                showProfile: false,
                editing: false,
                profile: {
                    username: "",
                    email: "",
                    first_name: "",
                    last_name: "",
                },

                searchCity: "",
                filterType: "",
                filterStartDate: "",
                filterEndDate: "",
                filterRadius: 10,
                currentLat: null,
                currentLon: null,
            };
        },
        computed: {
            ...mapState(["token"]),
            username() {
                return this.profile.username || "User";
            },
        },
        methods: {
            ...mapActions(["logout"]),
            handleLogout() {
                this.logout();
                this.$router.push("/");
            },
            openProfile() {
                this.showProfile = true;
                axios.get("/auth/me/").then((res) => {
                    this.profile = res.data;
                });
            },
            saveProfile() {
                axios
                    .put("/auth/me/", this.profile)
                    .then(() => {
                        this.editing = false;
                    })
                    .catch(() => {
                        alert("Error saving profile.");
                    });
            },
            searchByCity() {
                if (!this.searchCity) return;
                const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(
                    this.searchCity
                )}`;
                fetch(url)
                    .then((res) => res.json())
                    .then((data) => {
                        if (data.length > 0) {
                            const { lat, lon } = data[0];
                            this.map.setView(
                                [parseFloat(lat), parseFloat(lon)],
                                13
                            );
                        } else {
                            alert("City not found.");
                        }
                    });
            },
            loadAlerts() {
                const params = {};
                if (this.filterType) params.alert_type = this.filterType;
                if (this.filterStartDate)
                    params.start_date = this.filterStartDate;
                if (this.filterEndDate) params.end_date = this.filterEndDate;
                if (this.currentLat && this.currentLon && this.filterRadius) {
                    params.lat = this.currentLat;
                    params.lon = this.currentLon;
                    params.radius_km = this.filterRadius;
                }

                axios.get("/alerts/", { params }).then((res) => {
                    const geojson = {
                        type: "FeatureCollection",
                        features: res.data.features.map((feature) => {
                            // Verifica se o campo geometry é WKT
                            if (typeof feature.geometry === "string") {
                                const wkt = feature.geometry.replace(
                                    /^SRID=\d+;/,
                                    ""
                                ); // remove o SRID
                                feature.geometry = wellknown(wkt);
                            }
                            return feature;
                        }),
                    };

                    // Remove camada anterior
                    if (this.alertLayer) {
                        this.map.removeLayer(this.alertLayer);
                    }

                    // Cria camada nova
                    this.alertLayer = L.geoJSON(geojson, {
                        onEachFeature: (feature, layer) => {
                            const p = feature.properties;
                            layer.bindPopup(`
          <strong>Type:</strong> ${p.alert_type}<br>
          <strong>Description:</strong> ${p.description}<br>
          <strong>Summary:</strong> ${p.summary || "..."}<br>
          <strong>Created:</strong> ${new Date(p.created_at).toLocaleString()}
        `);
                        },
                    }).addTo(this.map);
                });
            },
        },
        mounted() {
            this.map = L.map("map").setView([40.4168, -3.7038], 6);
            L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
                attribution: "&copy; OpenStreetMap contributors",
            }).addTo(this.map);

            navigator.geolocation.getCurrentPosition(
                (pos) => {
                    this.currentLat = pos.coords.latitude;
                    this.currentLon = pos.coords.longitude;
                    this.map.setView([this.currentLat, this.currentLon], 12);
                    this.loadAlerts();
                },
                () => {
                    console.warn("User location not available");
                    this.loadAlerts();
                }
            );
        },
    };
</script>

<style scoped>
    .alert-map-page {
        font-family: "Segoe UI", sans-serif;
    }
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
    .filters {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        justify-content: center;
        margin-bottom: 1rem;
    }
    .form-input {
        padding: 0.5rem;
        border: 1px solid #ccc;
        border-radius: 8px;
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
