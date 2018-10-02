from .views import FoodViewSet
from common.routers import CustomRouter

router = CustomRouter(trailing_slash=False)
router.register(r'food', FoodViewSet)
urlpatterns = router.urls
