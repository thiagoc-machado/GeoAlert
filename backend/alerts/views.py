from rest_framework import viewsets, permissions
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Alert
from .serializers import AlertSerializer
from alerts.tasks import classify_and_summarize_alert
from core.mongo_logger import db
from .serializers import IAActionLogSerializer

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all().order_by('-created_at')
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        alert = serializer.save(user=self.request.user)
        classify_and_summarize_alert.delay(alert.id)

class IAActionLogViewSet(viewsets.ViewSet):
    serializer_class = IAActionLogSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        collection = db['ia_logs']
        logs = collection.find({'user_id': request.user.id}).sort('timestamp', -1)
        data = list(logs)
        for d in data:
            d['timestamp'] = d['timestamp'].isoformat()
        serializer = IAActionLogSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)