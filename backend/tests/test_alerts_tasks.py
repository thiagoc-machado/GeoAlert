# tests/test_alerts_tasks.py
import pytest
from alerts.tasks import classify_and_summarize_alert

@pytest.mark.django_db
def test_classify_and_summarize_alert(monkeypatch):
    def mock_post(url, headers, json):
        class MockResponse:
            def raise_for_status(self): pass
            def json(self):
                return {'choices': [{'message': {'content': 'This is a mock summary and classification'}}]}
        return MockResponse()

    monkeypatch.setattr('alerts.tasks.requests.post', mock_post)
    result = classify_and_summarize_alert(1, 'There was a fire on Main Street')
    assert 'choices' in result

@pytest.mark.django_db
def test_classify_and_summarize_alert_failure(monkeypatch):
    def mock_post(url, headers, json):
        raise Exception('Erro forçado no teste')

    monkeypatch.setattr('alerts.tasks.requests.post', mock_post)
    result = classify_and_summarize_alert(1, 'test')
    assert 'error' in result
    assert result['error'] == 'Erro forçado no teste'