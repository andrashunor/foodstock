from .views import IngredientViewSet
from common.routers import CustomRouter

router = CustomRouter(trailing_slash=False)
router.register(r'ingredient', IngredientViewSet)
urlpatterns = router.urls
