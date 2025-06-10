import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
import os

os.environ['CELERY_TASK_ALWAYS_EAGER'] = 'True'
os.environ['CELERY_TASK_EAGER_PROPAGATES'] = 'True'

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    def make_user(**kwargs):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': '12345678',
        }
        data.update(kwargs)
        return User.objects.create_user(**data)
    return make_user

@pytest.fixture
def get_token(api_client, create_user):
    def generate_token():
        user = create_user()
        response = api_client.post('/api/auth/login/', {
            'username': user.username,
            'password': '12345678'
        })
        token = response.data['access']
        return token, user
    return generate_token

@pytest.fixture
def authenticated_client(api_client, get_token):
    token, _ = get_token()
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client
