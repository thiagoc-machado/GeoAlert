# 🛰️ GeoAlert Backend

This is the backend for the **GeoAlert** project — a geographic alert system built with Django, Django REST Framework, and GeoDjango. It allows authenticated users to create, manage, and visualize georeferenced alerts (e.g., accidents, floods, construction).

---

## ⚙️ Technologies Used

- Python 3.10+
- Django 5.2
- Django REST Framework
- GeoDjango + PostGIS
- JWT Authentication (`djangorestframework-simplejwt`)
- MongoDB (for logs)
- Redis (for async tasks)
- Celery (for AI classification/summarization)
- Docker + Docker Compose
- Pytest + Coverage for testing
- Swagger via `drf-spectacular`

---

## 📁 Project Structure

```
backend/
├── geoalert/          # Main Django project
│   ├── __init__.py    # Celery auto-loads here
│   └── celery.py      # Celery configuration
├── alerts/            # Geo alerts app (GeoDjango)
│   ├── views_logs.py  # Mongo log viewer
├── users/             # Custom user + JWT + profile (auth/me)
├── tests/             # Centralized tests with fixtures
├── requirements.txt
├── Dockerfile
├── Makefile
├── pytest.ini
└── .env
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

Create a `.env` file or export directly:

```env
DEBUG=1
SECRET_KEY=your-secret-key
POSTGRES_DB=geoalert
POSTGRES_USER=geoalert_user
POSTGRES_PASSWORD=secret
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_TASK_ALWAYS_EAGER=False
CELERY_TASK_EAGER_PROPAGATES=False
MONGO_URI=mongodb://localhost:27017/
MONGO_DB_NAME=geoalert_logs
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

### 6. Access Swagger and Redoc Documentation

- Swagger UI: [http://localhost:8000/api/docs/swagger/](http://localhost:8000/api/docs/swagger/)
- Redoc: [http://localhost:8000/api/docs/redoc/](http://localhost:8000/api/docs/redoc/)
- Schema (YAML): [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/)

---

## 🔐 Authentication (JWT)

Implemented using `rest_framework_simplejwt`.

### Endpoints:

| Method | Endpoint                | Description              |
|--------|-------------------------|--------------------------|
| POST   | `/api/auth/register/`   | Register user            |
| POST   | `/api/auth/login/`      | Get JWT access token     |
| POST   | `/api/auth/refresh/`    | Refresh token            |
| GET    | `/api/auth/me/`         | Get logged-in user data  |
| PUT    | `/api/auth/me/`         | Update logged-in user    |

---

## 📍 Alerts API (GeoDjango)

Authenticated users can create and retrieve geographic alerts.

### Endpoints:

| Method | Endpoint                | Description               |
|--------|-------------------------|---------------------------|
| GET    | `/api/alerts/`          | List alerts (GeoJSON)     |
| POST   | `/api/alerts/`          | Create alert (GeoJSON)    |
| GET    | `/api/alerts/<id>/`     | Retrieve single alert     |

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

## 📊 IA Logs API (MongoDB)

Logs from AI tasks (classification/summarization) are stored in MongoDB and can be retrieved by the authenticated user.

### Endpoints:

| Method | Endpoint              | Description               |
|--------|-----------------------|---------------------------|
| GET    | `/api/alerts/logs/`   | List user's AI logs       |

---

## ⚙️ Background Tasks with Celery

GeoAlerts are automatically classified and summarized using an AI model (Groq API). This happens asynchronously via Celery + Redis.

### Task file:

```python
from celery import shared_task

@shared_task
def classify_and_summarize_alert(alert_id, description):
    ...
```

Tasks are mocked and tested with 100% coverage using Pytest.

---

## 🧪 Testing and Coverage

We use **pytest** and **pytest-django** with over 95% test coverage, including:

- Alerts CRUD
- Celery tasks (mocked)
- JWT authentication and user profile
- MongoDB log view
- Access control for protected routes

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

✅ 96%+ test coverage with `coverage.xml`

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

## ✅ Features Completed

- JWT-based auth (register/login/refresh)
- Profile management via `/auth/me/`
- GeoAlert CRUD with GeoDjango and GeoJSON
- Extensive test coverage with Pytest
- Swagger auto-docs with drf-spectacular
- Docker-ready environment
- Redis in isolated container
- Celery integration with background task and eager execution for tests
- AI-powered alert classification (mocked for now)
- MongoDB logs per authenticated user
- Access restriction tests (401 for unauthenticated users)
- Clean code and SOLID principles applied
- Frontend integrated with secure API

---

## 📌 Notes

- PostGIS runs inside Docker container
- GDAL installed locally for GeoDjango dev
- Frontend lives in `/frontend` (Vue 3 + Vite + Vuex)
- CORS enabled globally (`CORS_ALLOW_ALL_ORIGINS=True`)

---

## 📄 License

This project is open-source and can be reused for educational or commercial purposes under appropriate licensing terms.