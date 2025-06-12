from django.apps import AppConfig

class AlertsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'alerts'

    def ready(self):
        # Connect alert signals on app ready
        import alerts.signals
