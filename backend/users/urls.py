from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ProfileViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'register', UserViewSet, basename='register')
router.register(r'', ProfileViewSet, basename='profile')

urlpatterns = router.urls + [
    # JWT endpoints
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
