import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User
from core.mongo_logger import db
from datetime import datetime

@pytest.mark.django_db
def test_logs_view_returns_user_logs():
    user = User.objects.create_user(username='tester', email='tester@test.com', password='123456')
    client = APIClient()
    client.force_authenticate(user=user)

    db['ia_logs'].insert_one({
        'user_id': user.id,
        'type': 'summary',
        'input': {'text': 'fake input'},
        'result': {'text': 'fake result'},
        'timestamp': datetime.utcnow()
    })

    response = client.get('/api/logs/')

    assert response.status_code == 200
    assert isinstance(response.data, list)
    assert response.data[0]['type'] == 'summary'


@pytest.mark.django_db
def test_logs_view_requires_authentication():
    client = APIClient()
    response = client.get('/api/alerts/logs/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
