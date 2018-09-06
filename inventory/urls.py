from django.urls import path
from .views import FoodViewSet, LoginView, RegisterUsers, ClearUserFoodView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'food', FoodViewSet)
urls = router.urls
urls.append(path('foods/clear/', ClearUserFoodView.as_view(), name="foods-clear"))
urls.append(path('auth/login/', LoginView.as_view(), name="auth-login"))
urls.append(path('auth/register/', RegisterUsers.as_view(), name="auth-register"))
urlpatterns = urls
