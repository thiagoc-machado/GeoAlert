import requests
from django.conf import settings


def call_groq_api(description: str) -> str:
    """
    Send a prompt to Groq API to classify and summarize a geographic alert.
    """
    payload = {
        'model': settings.GROQ_MODEL,
        'messages': [
            {'role': 'system', 'content': 'You are a helpful assistant that classifies and summarizes geographic alerts.'},
            {'role': 'user', 'content': f'Description: {description}'}
        ]
    }
    headers = {
        'Authorization': f'Bearer {settings.GROQ_API_KEY}',
        'Content-Type': 'application/json'
    }

    response = requests.post(f'{settings.GROQ_ENDPOINT}chat/completions', json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        raise Exception(f'Groq API error: {response.status_code} - {response.text}')
