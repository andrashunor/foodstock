from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework import generics
from .models import Food
from .serializers import FoodSerializer


def index(request):
    return HttpResponse("Hello, my world!")
    
class ListCreateFoodView(generics.ListCreateAPIView):
    """
    GET food/
    POST food/
    """
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

    #validate_request_data
    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=request.data["user_id"])
        new_food = Food.objects.create(user=user, name=request.data["name"])
        return Response(data=FoodSerializer(new_food).data, status=status.HTTP_201_CREATED)
    
