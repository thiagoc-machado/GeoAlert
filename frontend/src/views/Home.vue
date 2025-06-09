<template>
  <div class="home">
    <section class="intro">
      <h1>🌍 Welcome to GeoAlert</h1>
      <p class="subtitle">
        A real-time system to monitor and visualize geographic alerts across the map.
      </p>

      <img
        src="https://media.istockphoto.com/id/1411803985/es/vector/mapa-mundial-detallado-con-pa%C3%ADses-divididos-en-un-fondo-transparente.jpg?s=612x612&w=0&k=20&c=yuW-w6_KdyH-mtSmobi949tlcY0zXxTPXM34CcNvYn0="
        alt="Map preview"
        class="map-image"
      />

      <div class="buttons">
        <router-link to="/login" class="btn primary">🔐 Login</router-link>
        <router-link to="/alerts-map" class="btn secondary">🗺️ View Map</router-link>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'Home'
}
</script>

<style scoped>
.home {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 2rem;
  background: linear-gradient(to bottom right, #eef2f3, #dff9fb);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #2c3e50;
}

.intro {
  max-width: 700px;
  text-align: center;
}

h1 {
  font-size: 2.8rem;
  margin-bottom: 1rem;
}

.subtitle {
  font-size: 1.2rem;
  margin-bottom: 2rem;
}

.map-image {
  width: 100%;
  max-width: 500px;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  margin: 0 auto 2rem;
}

.buttons {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.btn {
  padding: 0.9rem 1.8rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
}

.primary {
  background-color: #2980b9;
  color: #fff;
}

.primary:hover {
  background-color: #3498db;
}

.secondary {
  background-color: #2ecc71;
  color: #fff;
}

.secondary:hover {
  background-color: #27ae60;
}
</style>
