# 🛰️ GeoAlert Backend

This is the backend for the **GeoAlert** project — a geographic alert system built with Django, Django REST Framework, and GeoDjango. It allows authenticated users to create, manage, and visualize georeferenced alerts (e.g., accidents, floods, construction).

---

## ⚙️ Technologies Used

- Python 3.10+
- Django 5.2
- Django REST Framework
- GeoDjango + PostGIS
- JWT Authentication (`djangorestframework-simplejwt`)
- MongoDB (planned for logs)
- Redis (for async tasks, planned)
- Docker + Docker Compose
- Pytest + Coverage for testing

---

## 📁 Project Structure

```
backend/
├── geoalert/          # Main Django project
├── alerts/            # Geo alerts app (GeoDjango)
├── users/             # Custom user + JWT authentication
├── tests/             # Centralized tests with fixtures
├── requirements.txt
├── Dockerfile
├── Makefile
└── pytest.ini
```

---

## 🚀 How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/thiagoc-machado/GeoAlert.git
cd GeoAlert/backend
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file or use `export` commands. Example:

```env
DEBUG=1
SECRET_KEY=your-secret-key
POSTGRES_DB=geoalert
POSTGRES_USER=geoalert_user
POSTGRES_PASSWORD=secret
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### 4. Run migrations and create superuser

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Start the development server

```bash
python manage.py runserver
```

---

## 🧪 Testing and Coverage

We use **pytest** and **pytest-django** with 100% test coverage.

### Run tests

```bash
make test
```

### Generate coverage report

```bash
make coverage
```

### HTML coverage report

```bash
make coverage-html
xdg-open htmlcov/index.html
```

---

## 🔐 Authentication (JWT)

Implemented using `rest_framework_simplejwt`.

### Endpoints:

| Method | Endpoint              | Description           |
|--------|-----------------------|-----------------------|
| POST   | `/api/auth/register/` | Register user         |
| POST   | `/api/auth/login/`    | Get JWT access token  |
| POST   | `/api/auth/refresh/`  | Refresh token         |

---

## 📍 Alerts API (GeoDjango)

Authenticated users can create and retrieve geographic alerts.

### Endpoints:

| Method | Endpoint        | Description               |
|--------|------------------|---------------------------|
| GET    | `/api/alerts/`   | List alerts (GeoJSON)     |
| POST   | `/api/alerts/`   | Create alert (GeoJSON)    |
| GET    | `/api/alerts/<id>/` | Retrieve single alert |

### Example alert payload (GeoJSON):

```json
{
  "alert_type": "accident",
  "description": "Road blocked due to crash",
  "geometry": {
    "type": "Point",
    "coordinates": [-3.7038, 40.4168]
  }
}
```

---

## 🐳 Docker Usage (optional)

### Build and run services

```bash
make up
```

### Stop containers

```bash
make down
```

### Rebuild backend image

```bash
make build
```

---

## ✅ Test Coverage Summary

- Auth (register, login, refresh, invalid login)
- Alerts (create, list, retrieve, permissions)
- Custom model string representations (`__str__`)
- 100% coverage with `coverage.xml` report

---

## 📌 Notes

- PostGIS runs via Docker container
- GDAL installed locally for development
- Frontend is in `/frontend` (Vue 3 + Vite + Vuex)
- CORS enabled globally (`CORS_ALLOW_ALL_ORIGINS=True`)

---

## 📄 License

This project is open-source and can be reused for educational or commercial purposes under appropriate licensing terms.