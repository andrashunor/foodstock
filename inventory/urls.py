from django.urls import path
from . import views
from .views import ListCreateFoodView

urlpatterns = [
    path('', views.index, name='index'),
    path('foods/', ListCreateFoodView.as_view(), name="foods-all")
]
