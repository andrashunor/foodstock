from django.urls import path
from . import views
from .views import ListCreateFoodView, FoodDetailView, LoginView, RegisterUsers

urlpatterns = [
    path('', views.index, name='index'),
    path('foods/', ListCreateFoodView.as_view(), name="foods-all"),
    path('foods/id=<int:pk>/', FoodDetailView.as_view(), name="food-detail"),
    path('auth/login/', LoginView.as_view(), name="auth-login"),
    path('auth/register/', RegisterUsers.as_view(), name="auth-register")
]
