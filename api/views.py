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
from .decorators import validate_for_list_update
from .services import FoodService

# Get the JWT settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    
class FoodViewSet(ModelViewSet):
    
    """
    ViewSet for Food model
    GET food
    POST food
    DELETE food
    PUT food
    GET food/:id
    PUT food/:id
    PATCH food/:id
    DELETE food/:id
    """
    queryset = Food.objects.none()
    serializer_class = FoodSerializer
    permission_classes = (IsAuthenticated,)
    
    """
    Endpoints
    """
    
    def list(self, request):
        
        # GET /food
        service = FoodService()
        foods = service.get_foods(user=request.user)
        queryset = self.filter_queryset(foods)
        page = self.paginate_queryset(queryset)
        if page is not None:
            data = service.data(page, many=True)
            return self.get_paginated_response(data)

        return Response(service.data(queryset, many=True))

    def create(self, request):
        
        # POST /food
        many = isinstance(request.data, list)
        service = FoodService()
        new_food = service.create_food(request.data, user=request.user)
        return Response(data=service.data(new_food, many=many), status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        
        # GET /food/:id
        service = FoodService()
        result = service.get_food(pk, user=request.user)
        if isinstance(result, Exception):
            return Response(result.args[0], status=result.args[1])
        return Response(service.data(result), status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        
        # PUT /food/:id
        service = FoodService()
        result = service.update_food(pk, data=request.data, user=request.user)
        if isinstance(result, Exception):
            return Response(result.args[0], status=result.args[1])
        return Response(service.data(result), status=status.HTTP_200_OK)
        
    def partial_update(self, request, pk=None):
        
        # PATCH /food/:id
        service = FoodService()
        result = service.update_food(pk, data=request.data, partial=True, user=request.user)
        if isinstance(result, Exception):
            return Response(result.args[0], status=result.args[1])
        return Response(service.data(result), status=status.HTTP_200_OK)
    
    def destroy(self, request, pk=None):
        
        # DELETE /food/:id
        service = FoodService()
        result = service.delete_food(pk, user=request.user)
        if isinstance(result, Exception):
            return Response(result.args[0], status=result.args[1])
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    def delete_all(self, request):
        
        # GET /food?clear=true
        service = FoodService()
        result = service.clear_food_list(params=self.request.query_params, user=self.request.user)
        if isinstance(result, Exception):
            return Response(result.args[0], status=result.args[1])
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @validate_for_list_update
    def update_list(self, request):
        
        # PUT /food?many=true&ids=1,2,3
        service = FoodService()
        result = service.update_food_list(params=request.query_params, data=request.data, user=self.request.user)
        if isinstance(result, Exception):
            return Response(result.args[0], status=result.args[1])
        return Response(service.data(result, many=True), status=status.HTTP_200_OK)
    
    def partial_update_list(self, request):
        
        # PATCH /food?many=true&ids=1,2,3
        service = FoodService()
        result = service.update_food_list(params=request.query_params, data=request.data, partial=True, user=self.request.user)
        if isinstance(result, Exception):
            return Response(result.args[0], status=result.args[1])
        return Response(service.data(result, many=True), status=status.HTTP_200_OK)

class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """

    # This permission class will over ride the global permission
    # class setting
    serializer_class = UserSerializer
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
    serializer_class = UserSerializer
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
        