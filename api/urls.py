from django.urls import path
from .views import FoodViewSet, LoginView, RegisterUsers, ImageViewSet
from common.routers import CustomRouter

router = CustomRouter(trailing_slash=False)
router.register(r'food', FoodViewSet)
router.register(r'image', ImageViewSet)
urls = router.urls
urls.append(path('auth/login/', LoginView.as_view(), name="auth-login"))
urls.append(path('auth/register/', RegisterUsers.as_view(), name="auth-register"))
urlpatterns = urls