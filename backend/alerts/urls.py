from rest_framework.routers import DefaultRouter
from .views import AlertViewSet
from .views import IAActionLogViewSet

router = DefaultRouter()
router.register(r'alerts', AlertViewSet, basename='alerts')
router.register(r'logs', IAActionLogViewSet, basename='alerts-logs')

urlpatterns = router.urls
