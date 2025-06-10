# tests/test_alerts_tasks.py

import pytest
from alerts.models import Alert
from alerts.tasks import classify_and_summarize_alert
from users.models import User
from django.contrib.gis.geos import Point
from alerts.services import classify_text

@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )

@pytest.mark.django_db
def test_classify_and_summarize_alert(user):
    alert = Alert.objects.create(
        user=user,
        description='Flood in the area',
        geometry=Point(-3.7038, 40.4168)
    )
    classify_and_summarize_alert(alert.id, alert.description)
    alert.refresh_from_db()
    assert alert.alert_type == 'Flood'
    assert len(alert.summary) > 0

@pytest.mark.django_db
def test_classify_and_summarize_alert_failure(user, monkeypatch):
    alert = Alert.objects.create(
        user=user,
        description='This is a test',
        geometry=Point(-3.7038, 40.4168)
    )

    def mock_classify_text(text):
        raise Exception('Erro forçado no teste')

    monkeypatch.setattr('alerts.services.classify_text', mock_classify_text)

    with pytest.raises(Exception) as e:
        classify_and_summarize_alert(alert.id, alert.description)
    
    assert 'Erro forçado no teste' in str(e.value)

def test_classify_text_general():
    result = classify_text('This is a generic event')
    assert result == 'General'
