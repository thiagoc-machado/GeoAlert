# alerts/management/commands/generate_fake_alerts.py
import random
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from django.contrib.auth import get_user_model
from alerts.models import Alert
from alerts.tasks import classify_and_summarize_alert

class Command(BaseCommand):
    help = 'Generate random fake alerts for testing'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=10, help='Number of alerts to generate')

    def handle(self, *args, **options):
        count = options['count']
        User = get_user_model()
        user = User.objects.first()

        if not user:
            self.stdout.write(self.style.ERROR('No user found. Create a user first.'))
            return

        alert_types = ['flood', 'fire', 'construction']
        descriptions = [
            'A dangerous situation has been reported in the area.',
            'Multiple reports of issues from citizens.',
            'Emergency teams are already on site.',
            'Situation is under control but monitoring continues.',
            'Damage to infrastructure reported.'
        ]

        for i in range(count):
            lat = random.uniform(39.0, 40.5)   # Simulated range (Spain)
            lon = random.uniform(-4.5, -0.5)
            alert = Alert.objects.create(
                user=user,
                alert_type=random.choice(alert_types),
                description=random.choice(descriptions),
                geometry=Point(lon, lat, srid=4326)
            )
            classify_and_summarize_alert.delay(alert.id)

        self.stdout.write(self.style.SUCCESS(f'{count} fake alerts created.'))
