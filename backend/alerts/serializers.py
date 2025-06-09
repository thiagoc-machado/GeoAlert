from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Alert

class AlertSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Alert
        geo_field = 'geometry'
        fields = ('id', 'alert_type', 'description', 'geometry', 'created_at')
