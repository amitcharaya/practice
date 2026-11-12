from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserManagementViewSet, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
router = DefaultRouter()
router.register(r'users', UserManagementViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),

    # Custom JWT + 2FA Login API
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
