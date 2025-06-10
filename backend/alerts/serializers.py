from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Alert
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

@extend_schema_field(serializers.JSONField())
class AlertSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Alert
        geo_field = 'geometry'
        fields = ('id', 'alert_type', 'description', 'geometry', 'created_at')

class IAActionLogSerializer(serializers.Serializer):
    type = serializers.CharField()
    input = serializers.JSONField()
    result = serializers.JSONField()
    timestamp = serializers.DateTimeField()