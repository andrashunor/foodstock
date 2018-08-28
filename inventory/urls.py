from django.urls import path
from . import views
from .views import ListFoodsView

urlpatterns = [
    path('', views.index, name='index'),
    path('foods/', ListFoodsView.as_view(), name="foods-all")
]
