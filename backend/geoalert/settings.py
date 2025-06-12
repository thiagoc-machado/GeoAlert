import os
from pathlib import Path
from datetime import timedelta
from decouple import config, Csv

os.environ.setdefault(
    'GDAL_LIBRARY_PATH',
    '/usr/lib/x86_64-linux-gnu/libgdal.so.35'
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = config('DJANGO_SECRET_KEY', default='insecure-secret')
DEBUG = config('DJANGO_DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.gis',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_extensions',
    'django_celery_beat',
    'drf_spectacular',

    'core',
    'alerts',
    'users',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'geoalert.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'geoalert.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('POSTGRES_HOST', default='db'),
        'PORT': config('POSTGRES_PORT', default='5432'),
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Timezone / Language
TIME_ZONE = config('TIME_ZONE', default='Europe/Madrid')
LANGUAGE_CODE = config('LANGUAGE_CODE', default='en-us')

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

CORS_ALLOW_ALL_ORIGINS = True


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(seconds=config('SIMPLE_JWT_ACCESS_TOKEN_LIFETIME', default=3600, cast=int)),
    'REFRESH_TOKEN_LIFETIME': timedelta(seconds=config('SIMPLE_JWT_REFRESH_TOKEN_LIFETIME', default=86400, cast=int)),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

AUTH_USER_MODEL = 'users.User'

# Celery
CELERY_BROKER_URL = config('CELERY_BROKER_URL')
CELERY_TASK_ALWAYS_EAGER = config('CELERY_TASK_ALWAYS_EAGER', default=False, cast=bool)
CELERY_TASK_EAGER_PROPAGATES = config('CELERY_TASK_EAGER_PROPAGATES', default=False, cast=bool)

# MongoDB
MONGO_URI = config('MONGO_URI', default='mongodb://localhost:27017')
MONGO_DB_NAME = config('MONGO_DB_NAME', default='geoalert')

# GROQ API
GROQ_API_KEY = config('GROQ_API_KEY')
GROQ_MODEL = config('GROQ_MODEL')
GROQ_ENDPOINT = config('GROQ_ENDPOINT', default='https://api.groq.com/v1/')


# GDAL
GDAL_LIBRARY_PATH = config('GDAL_LIBRARY_PATH', default='/usr/lib/libgdal.so')
