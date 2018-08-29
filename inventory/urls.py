from django.urls import path
from . import views
from .views import ListCreateFoodView, FoodDetailView

urlpatterns = [
    path('', views.index, name='index'),
    path('foods/', ListCreateFoodView.as_view(), name="foods-all"),
    path('foods/id=<int:pk>/', FoodDetailView.as_view(), name="food-detail")
]
