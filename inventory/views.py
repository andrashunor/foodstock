from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, my world!")

from rest_framework import generics
from .models import Food
from .serializers import FoodSerializer


class ListFoodsView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
