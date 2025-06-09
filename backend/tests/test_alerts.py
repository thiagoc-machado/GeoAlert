import pytest
from django.contrib.gis.geos import Point
from alerts.models import Alert

@pytest.mark.django_db
def test_create_alert(authenticated_client):
    payload = {
        'alert_type': 'accident',
        'description': 'Test accident',
        'geometry': Point(0.0, 0.0).geojson
    }
    response = authenticated_client.post('/api/alerts/', payload, format='json')
    assert response.status_code == 201
    assert response.data['properties']['alert_type'] == 'accident'

@pytest.mark.django_db
def test_alert_requires_authentication(api_client):
    response = api_client.get('/api/alerts/')
    assert response.status_code == 401

@pytest.mark.django_db
def test_list_alerts(authenticated_client):
    # cria um alerta
    authenticated_client.post('/api/alerts/', {
        'alert_type': 'flood',
        'description': 'Rio subiu',
        'geometry': Point(1.0, 1.0).geojson
    }, format='json')

    response = authenticated_client.get('/api/alerts/')
    assert response.status_code == 200
    assert len(response.data['features']) >= 1

@pytest.mark.django_db
def test_retrieve_alert(authenticated_client):
    create = authenticated_client.post('/api/alerts/', {
        'alert_type': 'construction',
        'description': 'Obra em andamento',
        'geometry': Point(2.0, 2.0).geojson
    }, format='json')
    alert_id = create.data['id']
    response = authenticated_client.get(f'/api/alerts/{alert_id}/')
    assert response.status_code == 200
    assert response.data['properties']['alert_type'] == 'construction'

@pytest.mark.django_db
def test_create_alert_invalid_data(authenticated_client):
    response = authenticated_client.post('/api/alerts/', {
        'alert_type': 'invalid_type',
        'description': 'erro',
        'geometry': Point(0.0, 0.0).geojson
    }, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_alert_str(authenticated_client):
    response = authenticated_client.post('/api/alerts/', {
        'alert_type': 'accident',
        'description': 'Teste para __str__',
        'geometry': Point(3.0, 3.0).geojson
    }, format='json')
    from alerts.models import Alert
    alert = Alert.objects.get(id=response.data['id'])
    assert str(alert) == f'accident - {alert.created_at.date()}'

@pytest.mark.django_db
def test_alert_str_representation(authenticated_client):
    response = authenticated_client.post('/api/alerts/', {
        'alert_type': 'flood',
        'description': 'Para testar o __str__',
        'geometry': Point(-1.0, -1.0).geojson
    }, format='json')

    from alerts.models import Alert
    alert = Alert.objects.get(id=response.data['id'])
    expected_str = f'{alert.alert_type} - {alert.created_at.date()}'
    assert str(alert) == expected_str
