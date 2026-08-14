from rest_framework.routers import DefaultRouter
from .views import JailViewSet, SHGViewSet, VegetableMasterViewSet
from .views import BulkUploadViewSet

router = DefaultRouter()
router.register(r'jails', JailViewSet)
router.register(r'shgs', SHGViewSet)
router.register(r'vegetables', VegetableMasterViewSet)
router.register(
    r"bulk-upload",
    BulkUploadViewSet,
    basename="bulk-upload"
)


urlpatterns = router.urls