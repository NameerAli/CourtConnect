from rest_framework.routers import DefaultRouter
from .views import CourtViewSet, CourtImageViewSet, CourtAvailabilityViewSet

router = DefaultRouter()
router.register(r'courts', CourtViewSet, basename='court')
router.register(r'court-images', CourtImageViewSet, basename='court-image')
router.register(r'court-availability', CourtAvailabilityViewSet, basename='court-availability')

urlpatterns = router.urls
