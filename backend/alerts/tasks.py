
from celery import shared_task
import requests
from django.conf import settings
from core.mongo_logger import log_ia_action
from alerts.models import Alert

@shared_task
def classify_and_summarize_alert(alert_id, description):
    from alerts.services import classify_text, summarize_text

    alert = Alert.objects.get(id=alert_id)
    classification = classify_text(description)
    summary = summarize_text(description)

    alert.alert_type = classification
    alert.summary = summary
    alert.save()

    # Salvar log no MongoDB
    log_ia_action(
        user_id=alert.user.id,
        action_type='classification_summary',
        input_data={'description': description},
        result_data={'classification': classification, 'summary': summary}
    )

