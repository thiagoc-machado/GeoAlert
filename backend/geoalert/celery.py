# geoalert/celery.py

import os
from celery import Celery

# 🔁 Forçar modo síncrono no pytest (evita erro de conexão com Redis nos testes)
if 'PYTEST_CURRENT_TEST' in os.environ:
    os.environ.setdefault('CELERY_TASK_ALWAYS_EAGER', 'True')
    os.environ.setdefault('CELERY_TASK_EAGER_PROPAGATES', 'True')

# Config padrão do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geoalert.settings')

app = Celery('geoalert')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
