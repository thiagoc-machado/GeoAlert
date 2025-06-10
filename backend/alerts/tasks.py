
from celery import shared_task
import requests
from django.conf import settings

@shared_task
def classify_and_summarize_alert(alert_id, description):
    headers = {'Authorization': f'Bearer {settings.GROQ_API_KEY}'}
    payload = {
        'model': settings.GROQ_MODEL,
        'messages': [
            {'role': 'system', 'content': 'You are an assistant that classifies alerts and generates summaries.'},
            {'role': 'user', 'content': description}
        ]
    }
    try:
        response = requests.post('https://api.groq.com/openai/v1/chat/completions', headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        return {'error': str(e)}
