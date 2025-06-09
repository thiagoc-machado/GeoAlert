from django.contrib.gis.db import models
from django.conf import settings

class Alert(models.Model):
    TYPE_CHOICES = [
        ('accident', 'Accident'),
        ('construction', 'Construction'),
        ('flood', 'Flood'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    description = models.TextField()
    geometry = models.GeometryField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.alert_type} - {self.created_at.date()}'
