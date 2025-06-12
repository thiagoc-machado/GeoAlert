from django.contrib import admin
from .models import Alert
from django.contrib.gis.admin import GISModelAdmin

@admin.register(Alert)
class AlertAdmin(GISModelAdmin):
    list_display = ('id', 'user', 'alert_type', 'created_at')
    list_filter = ('alert_type', 'created_at')
    search_fields = ('description', 'summary', 'user__username')
