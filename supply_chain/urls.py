from rest_framework.routers import DefaultRouter

from .views import ReadCreateDemandViewSet
from django.urls import path, include
router = DefaultRouter()

router.register(r'demands', ReadCreateDemandViewSet)


urlpatterns = [
    path('', include(router.urls)),
    
    
]