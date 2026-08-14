from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserManagementViewSet, CustomTokenObtainPairView

router = DefaultRouter()
router.register(r'users', UserManagementViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),

    # Custom JWT + 2FA Login API
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
