from .views import ImageViewSet
from common.routers import CustomRouter

router = CustomRouter(trailing_slash=False)
router.register(r'image', ImageViewSet)
urlpatterns = router.urls