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
from rest_framework.viewsets import ModelViewSet


# Get the JWT settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

def index(request):
    return HttpResponse("Hello, my world!")
    
class FoodViewSet(ModelViewSet):
    
    """
    ViewSet for Food model
    POST food/
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
    
    def not_found_response(self, pk=None):
        return Response(data={"message": "Food with id: {} does not exist".format(pk)}, status=status.HTTP_404_NOT_FOUND)   
     
    def list(self, request):
        food_list = self.serializer_class(self.get_queryset(), many=True)
        return Response(food_list.data, status=status.HTTP_200_OK)

    def create(self, request):
        
        if not isinstance(request.data, list):
            
            # Single object creation
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            new_food = Food.objects.create(user=request.user, name=request.data["name"])
            return Response(data=FoodSerializer(new_food).data, status=status.HTTP_201_CREATED)
        
        
        # List creation
        serializer = self.get_serializer(data=request.data, many=True)
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
    
    def retrieve(self, request, pk=None):
        try:
            a_food = self.get_queryset().get(pk=pk)
            return Response(self.serializer_class(a_food).data, status=status.HTTP_200_OK)
        except Food.DoesNotExist:
            return self.not_found_response(pk=pk) 

    def update(self, request, pk=None):
        try:
            a_food = self.get_queryset().get(pk=pk)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            updated_food = serializer.update(a_food, request.data)
            return Response(FoodSerializer(updated_food).data)
        except Food.DoesNotExist:
            return self.not_found_response(pk=pk)
        
    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None, **kwargs):
        try:
            a_food = self.get_queryset().get(pk=pk)
            a_food.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Food.DoesNotExist:
            return self.not_found_response(pk=pk)
    
class ClearUserFoodView(generics.RetrieveUpdateDestroyAPIView):
    """
    POST foods/clear/
    API endpoint that allows user to clear all foods
    """
    queryset = Food.objects.none()
    serializer_class = FoodSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Food.objects.none()
        return Food.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        self.get_queryset().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        
        # Food update here
        foods_updated = []
        for list_elt in request.data:
            try:
                a_food = self.get_queryset().get(pk=kwargs["pk"])
                updated_food = serializer.update(a_food,  **list_elt)
                foods_updated.append(updated_food.id)
            except Food.DoesNotExist:
                return Response(
                    data={
                        "message": "Food with id: {} does not exist".format(kwargs["pk"])
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        results = Food.objects.filter(id__in=foods_updated)
        output_serializer = FoodSerializer(results, many=True)
        data = output_serializer.data[:]
        return Response(data, status=status.HTTP_201_CREATED)

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
        