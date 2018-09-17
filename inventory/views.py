from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db.models import Model

from rest_framework.response import Response
from rest_framework.views import status
from rest_framework import generics, permissions
from rest_framework_jwt.settings import api_settings

from .models import Food
from .serializers import FoodSerializer, TokenSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .decorators import validate_for_list_update

# Get the JWT settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

def update_object(view=ModelViewSet, model=Model, request=None, pk=None, partial=False):
    try:
        an_object = view.get_queryset().get(pk=pk)
        updated_serializer = view.get_serializer(an_object, data=request.data, partial=partial)
        updated_serializer.is_valid(raise_exception=True)
        updated_serializer.save()
        return Response(updated_serializer.data)
    except model.DoesNotExist:
        
        # Check for custom not found response on viewset
        not_found_response = getattr(view, "not_found_response", None)
        if callable(not_found_response):
            return view.not_found_response(pk=pk)
        
        # Send back default not found response
        return Response(data={"message": "{} with id: {} does not exist".format(model._meta.object_name, pk)}, status=status.HTTP_404_NOT_FOUND)
    
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
    
    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Food.objects.none()
        return Food.objects.filter(user=self.request.user)
    
    def not_found_response(self, pk=None):
        return Response(data={"message": "Food with id: {} does not exist".format(pk)}, status=status.HTTP_404_NOT_FOUND)
    
    """
    Endpoints
    """
    
    def list(self, request):
        
        # GET /food
        # Note: This is the default behavior defined in 'ListModelMixin' and deleting 'def list' would not change the behavior of the API. The code is only kept to provide an example.
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        
        # POST /food
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
        
        # GET /food/:id
        try:
            a_food = self.get_queryset().get(pk=pk)
            return Response(self.serializer_class(a_food).data, status=status.HTTP_200_OK)
        except Food.DoesNotExist:
            return self.not_found_response(pk=pk) 

    def update(self, request, pk=None):
        
        # PUT /food/:id
        return update_object(self, Food, request, pk)
        
    def partial_update(self, request, pk=None):
        
        # PATCH /food/:id
        return update_object(self, Food, request, pk, partial=True)

    def destroy(self, request, pk=None):
        
        # DELETE /food/:id
        try:
            a_food = self.get_queryset().get(pk=pk)
            a_food.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Food.DoesNotExist:
            return self.not_found_response(pk=pk)
        
    def delete_all(self, request):
        
        # GET /food?clear=true
        if 'clear' in request.query_params:
            if request.query_params["clear"]:
                self.get_queryset().delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    @validate_for_list_update
    def update_list(self, request):
        
        # PUT /food?many=true&ids=1,2,3
        serializer = self.get_serializer(data=request.data, many=True, partial=False)
        serializer.is_valid(raise_exception=True)
        ids = request.query_params['ids'].split(',')
        updated_data = serializer.update(ids, request.data)
        return Response(updated_data)
    
    @validate_for_list_update
    def partial_update_list(self, request):
        
        # PATCH /food?many=true&ids=1,2,3
        serializer = self.get_serializer(data=request.data, many=True, partial=True)
        serializer.is_valid(raise_exception=True)
        ids = request.query_params['ids'].split(',')
        updated_data = serializer.update(ids, request.data)
        return Response(updated_data)

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
        