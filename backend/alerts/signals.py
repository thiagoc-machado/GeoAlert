from django.db.models.signals import post_save
from django.dispatch import receiver
from alerts.models import Alert
from alerts.tasks import classify_and_summarize_alert


@receiver(post_save, sender=Alert)
def handle_alert_created(sender, instance, created, **kwargs):
    """
    Signal to trigger classification task when a new alert is created.
    """
    if created:
        classify_and_summarize_alert.delay(instance.id)
