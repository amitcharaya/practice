from rest_framework.routers import DefaultRouter
from .views import HotelViewSet, SHGViewSet, VegetableMasterViewSet
from .views import BulkUploadViewSet,VegetableBulkUploadView,HotelListCreateView
from django.urls import path, include
router = DefaultRouter()
router.register(r'jails', HotelViewSet)
router.register(r'shgs', SHGViewSet)
router.register(r'vegetables', VegetableMasterViewSet)

router.register(
    r"bulk-upload",
    BulkUploadViewSet,
    basename="bulk-upload"
)



urlpatterns = [
    path('', include(router.urls)),
    path(
        'bulk-upload-api/vegetables/',
        VegetableBulkUploadView.as_view(),
        name='vegetable-bulk-upload-api'
    ),
    path(
            'hotels/',
            HotelListCreateView.as_view(),
            name='list-active-hotels-api'
        ),
    
]