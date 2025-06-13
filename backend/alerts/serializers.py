from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Alert
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from django.contrib.gis.geos import GEOSGeometry

class AlertSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Alert
        geo_field = 'geometry'
        fields = '__all__'
        read_only_fields = ['user']

    # def to_internal_value(self, data):
    #     data = data.copy()
    #     geometry = data.get('geometry')
    #     if geometry:
    #         data['geometry'] = GEOSGeometry(str(geometry))
    #     return super().to_internal_value(data)

class IAActionLogSerializer(serializers.Serializer):
    type = serializers.CharField()
    input = serializers.JSONField()
    result = serializers.JSONField()
    timestamp = serializers.DateTimeField()
