
from celery import shared_task
import requests
from django.conf import settings
from core.mongo_logger import log_ia_action
from alerts.models import Alert
from alerts.services.groq_service import call_groq_api

@shared_task
def classify_and_summarize_alert(alert_id):
    from alerts.services import classify_text, summarize_text
    from core.services.mongo_logger import log_ia_action
    from alerts.models import Alert

    try:
        alert = Alert.objects.get(id=alert_id)
        description = alert.description

        classification = classify_text(description)
        summary = summarize_text(description)

        alert.alert_type = classification
        alert.summary = summary
        alert.save()

        # Save log to MongoDB
        log_ia_action(
            user_id=alert.user.id,
            action_type='classification_summary',
            input_data={'description': description},
            result_data={'classification': classification, 'summary': summary}
        )
    except Exception as e:
        print(f'Error processing alert {alert_id}: {str(e)}')


@shared_task
def classify_and_summarize_alert(alert_id):
    """
    Celery task to classify and summarize a geographic alert using Groq API.
    """
    try:
        alert = Alert.objects.get(id=alert_id)
        if alert.description:
            summary = call_groq_api(alert.description)
            alert.summary = summary  # You can adapt this to `alert.classification` if needed
            alert.save()
    except Alert.DoesNotExist:
        print(f'Alert with ID {alert_id} not found.')
    except Exception as e:
        print(f'Error processing alert {alert_id}: {str(e)}')