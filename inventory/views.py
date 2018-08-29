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
    GET foods/
    POST food/
    """
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

    #validate_request_data
    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=request.data["user_id"])
        new_food = Food.objects.create(user=user, name=request.data["name"])
        return Response(data=FoodSerializer(new_food).data, status=status.HTTP_201_CREATED)
    
class FoodDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET food/:id/
    PUT food/:id/
    DELETE food/:id/
    """
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

    def get(self, request, *args, **kwargs):
        try:
            a_food = self.queryset.get(pk=kwargs["pk"])
            return Response(FoodSerializer(a_food).data)
        except Food.DoesNotExist:
            return Response(
                data={
                    "message": "Food with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

#     @validate_request_data
    def put(self, request, *args, **kwargs):
        try:
            a_food = self.queryset.get(pk=kwargs["pk"])
            serializer = FoodSerializer()
            updated_food = serializer.update(a_food, request.data)
            return Response(FoodSerializer(updated_food).data)
        except Food.DoesNotExist:
            return Response(
                data={
                    "message": "Food with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_food = self.queryset.get(pk=kwargs["pk"])
            a_food.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Food.DoesNotExist:
            return Response(
                data={
                    "message": "Food with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )
