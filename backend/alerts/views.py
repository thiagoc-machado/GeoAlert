from rest_framework import viewsets, permissions
from .models import Alert
from .serializers import AlertSerializer
from alerts.tasks import classify_and_summarize_alert

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all().order_by('-created_at')
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        alert = serializer.save(user=self.request.user)
        classify_and_summarize_alert.delay(alert.id, alert.description)
