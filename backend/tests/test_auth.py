import pytest

@pytest.mark.django_db
def test_register_user(api_client):
    response = api_client.post('/api/auth/register/', {
        'username': 'newuser',
        'email': 'new@example.com',
        'password': '123456'
    })
    assert response.status_code == 201
    assert 'id' in response.data

@pytest.mark.django_db
def test_login_user(api_client, create_user):
    create_user(username='thiago', password='abc123')
    response = api_client.post('/api/auth/login/', {
        'username': 'thiago',
        'password': 'abc123'
    })
    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data

@pytest.mark.django_db
def test_login_invalid_credentials(api_client):
    response = api_client.post('/api/auth/login/', {
        'username': 'invalido',
        'password': 'senhaerrada'
    })
    assert response.status_code == 401

@pytest.mark.django_db
def test_refresh_token(api_client, get_token):
    _, user = get_token()
    login = api_client.post('/api/auth/login/', {
        'username': user.username,
        'password': '12345678'
    })
    refresh_token = login.data['refresh']
    response = api_client.post('/api/auth/refresh/', {
        'refresh': refresh_token
    })
    assert response.status_code == 200
    assert 'access' in response.data

@pytest.mark.django_db
def test_get_logged_user(authenticated_client):
    response = authenticated_client.get('/api/auth/me/')
    assert response.status_code == 200
    assert 'username' in response.data

@pytest.mark.django_db
def test_update_profile(authenticated_client):
    response = authenticated_client.put('/api/auth/me/', {
        'first_name': 'Thiago',
        'last_name': 'Machado',
        'email': 'thiago@geoalert.com'
    })
    assert response.status_code == 200
    assert response.data['first_name'] == 'Thiago'