from rest_framework import viewsets, permissions
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
from .models import Alert
from .serializers import AlertSerializer
from alerts.tasks import classify_and_summarize_alert
from core.mongo_logger import db
from .serializers import IAActionLogSerializer

class AlertViewSet(viewsets.ModelViewSet):
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Alert.objects.all().order_by('-created_at')

        alert_type = self.request.query_params.get('alert_type')
        if alert_type:
            queryset = queryset.filter(alert_type=alert_type)

        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(created_at__gte=make_aware(parse_datetime(start_date)))
        if end_date:
            queryset = queryset.filter(created_at__lte=make_aware(parse_datetime(end_date)))

        lat = self.request.query_params.get('lat')
        lon = self.request.query_params.get('lon')
        radius_km = self.request.query_params.get('radius_km')

        if lat and lon and radius_km:
            user_location = Point(float(lon), float(lat), srid=4326)
            queryset = queryset.annotate(distance=Distance('geometry', user_location))
            queryset = queryset.filter(distance__lte=float(radius_km) * 1000)

        return queryset

    def perform_create(self, serializer):
        alert = serializer.save(user=self.request.user)
        classify_and_summarize_alert.delay(alert.id)

class IAActionLogViewSet(viewsets.ViewSet):
    serializer_class = IAActionLogSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        collection = db['ia_logs']
        logs = collection.find({'user_id': request.user.id})
        data = [
            {
                'type': log['action_type'],
                'input': log['input_data'],
                'result': log['result_data'],
                'timestamp': log['timestamp']
            } for log in logs
        ]
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data)
