from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from rest_framework.response import Response
from rest_framework.views import status
from rest_framework import generics, permissions
from rest_framework_jwt.settings import api_settings

from .models import Food
from .serializers import FoodSerializer, TokenSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated


# Get the JWT settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

def index(request):
    return HttpResponse("Hello, my world!")
    
class ListCreateFoodView(generics.ListCreateAPIView):
    """
    GET foods/
    POST foods/
    """
    queryset = Food.objects.none()
    serializer_class = FoodSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Food.objects.none()
        return Food.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_food = Food.objects.create(user=request.user, name=request.data["name"])
        return Response(data=FoodSerializer(new_food).data, status=status.HTTP_201_CREATED)
    
    
class CreateFoodBatchView(generics.ListCreateAPIView):
    """
    POST foods/batch/
    API endpoint that allows multiple members to be created.
    """
    queryset = Food.objects.none()
    serializer_class = FoodSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Food.objects.none()
        return Food.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        
#         # Only include a single error if required
#         if serializer.errors:
#             
#             error = serializer.errors[0]
#             return Response(
#                 data={
#                     "message": error["message"][0]
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )

        food_created = []
        for list_elt in request.data:
            food_obj = Food.objects.create(user=request.user, **list_elt)
            food_created.append(food_obj.id)
        results = Food.objects.filter(id__in=food_created)
        output_serializer = FoodSerializer(results, many=True)
        data = output_serializer.data[:]
        return Response(data, status=status.HTTP_201_CREATED)
    
class ClearUserFoodView(generics.DestroyAPIView):
    """
    POST foods/clear/
    API endpoint that allows user to clear all foods
    """
    queryset = Food.objects.none()
    serializer_class = FoodSerializer
    permission_classes = (IsAuthenticated,)
    
    def delete(self, request, *args, **kwargs):
        user_foods = Food.objects.filter(user=request.user)
        user_foods.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class FoodDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET food/:id/
    PUT food/:id/
    DELETE food/:id/
    """
    queryset = Food.objects.none()
    serializer_class = FoodSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Food.objects.none()
        return Food.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        try:
            a_food = self.get_queryset().get(pk=kwargs["pk"])
            return Response(FoodSerializer(a_food).data)
        except Food.DoesNotExist:
            return Response(
                data={
                    "message": "Food with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            a_food = self.get_queryset().get(pk=kwargs["pk"])
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
            a_food = self.get_queryset().get(pk=kwargs["pk"])
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
        