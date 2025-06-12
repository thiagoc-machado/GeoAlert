# 🗺️ GeoAlert Frontend

This is the frontend for the **GeoAlert** project — a geographic alert system that allows users to register, login, and view real-time geographic alerts on an interactive map.

---

## ⚙️ Technologies Used

- Vue 3
- Vuex
- Vue Router
- Leaflet.js
- Axios (with JWT interceptor)
- Vite
- Vitest (for testing)
- CSS Modules + scoped styles
- Docker + Docker Compose (for development)
- Hot reload with Vite and Dockerfile.dev

---

## 📁 Project Structure

```
frontend/
├── public/                      # Static assets (favicon, images)
├── src/
│   ├── assets/                  # Global styles
│   ├── views/                   # Pages (Home, Login, AlertMap)
│   ├── store/                   # Vuex token store
│   ├── router/                  # Vue Router setup
│   ├── axios.js                 # Axios with JWT support
│   └── main.js                  # App entry
├── tests/                       # Unit tests with Vitest
├── vite.config.js
├── Dockerfile                  # Production build (with Nginx)
├── Dockerfile.dev              # Development with Vite hot reload
```

---

## 🚀 How to Run Locally

```bash
cd frontend
npm install
npm run dev
```

Frontend available at: [http://localhost:5173](http://localhost:5173)

Or using Docker Compose (dev):

```bash
docker-compose -f docker-compose.dev.yml up -d frontend
```

---

## 🔐 Authentication Flow

- Login via `/api/auth/login/`
- JWT stored in Vuex + localStorage
- Axios interceptor attaches `Authorization: Bearer <token>` automatically
- Protected routes redirect to `/login` if unauthenticated

---

## 📍 Features Implemented

- ✅ Home Page (`/`) with explanation and call-to-action
- ✅ Login Page with JWT auth
- ✅ Protected map view (`/alerts-map`) showing alerts
- ✅ Leaflet integration with GeoJSON data
- ✅ Global Axios instance with interceptor
- ✅ Vuex for token storage and logout
- ✅ Top bar with user name and logout
- ✅ Modal to view/edit user profile via `/auth/me/`
- ✅ Favicon and HTML metadata updated
- ✅ Responsive design with consistent UX
- ✅ Tests with **Vitest** and 100% pass rate
- ✅ `Dockerfile.dev` with Vite hot reload for development
- ✅ `Dockerfile` for static production build with Nginx

---

## 🧪 Testing with Vitest

```bash
npm run test
npx vitest --ui
```

Tests include:

- Home.vue – render check
- Login.vue – input, login, error handling
- AlertMap.vue – map render, modal, user load
- Axios mocked for profile + alerts
- 100% test coverage achieved ✅

---

## 🐳 Docker Usage

### Development (hot reload with Vite)

```bash
docker-compose -f docker-compose.dev.yml up -d frontend
```

### Production (static build with Nginx)

```bash
docker-compose up -d frontend
```

---

## 🖼️ UI Preview

- Landing page with image + description
- Leaflet map with alert markers
- Responsive modals for profile
- Modern buttons, colors, layout

---

## 📄 License

This project is open-source and free to use under proper license terms.
