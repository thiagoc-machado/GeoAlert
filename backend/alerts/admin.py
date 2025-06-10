from django.contrib import admin
from .models import Alert

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'alert_type', 'created_at')
    list_filter = ('alert_type', 'created_at')
    search_fields = ('description', 'summary', 'user__username')
