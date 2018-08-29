from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from rest_framework.response import Response
from rest_framework.views import status
from rest_framework import generics, permissions
from rest_framework_jwt.settings import api_settings

from .decorators import validate_request_data
from .models import Food
from .serializers import FoodSerializer, TokenSerializer, UserSerializer

# Get the JWT settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

def index(request):
    return HttpResponse("Hello, my world!")
    
class ListCreateFoodView(generics.ListCreateAPIView):
    """
    GET foods/
    POST food/
    """
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

    @validate_request_data
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

    @validate_request_data
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

class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """

    # This permission class will over ride the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)
            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class RegisterUsers(generics.CreateAPIView):
    """
    POST auth/register/
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        email = request.data.get("email", "")
        if not username and not password and not email:
            return Response(
                data={
                    "message": "username, password and email is required to register a user"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        new_user = User.objects.create_user(
            username=username, password=password, email=email
        )
        return Response(
            data=UserSerializer(new_user).data,
            status=status.HTTP_201_CREATED
        )
        