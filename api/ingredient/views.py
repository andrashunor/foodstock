from .serializers import IngredientSerializer
from .models import Ingredient
from rest_framework.permissions import IsAuthenticated
from .services import IngredientService
from common.views import ServiceModelViewSet
from rest_framework.views import status
from rest_framework.response import Response

class IngredientViewSet(ServiceModelViewSet):
    
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    service_class = IngredientService
    permission_classes = (IsAuthenticated,)