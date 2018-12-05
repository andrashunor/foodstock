from .serializers import IngredientSerializer
from .models import Ingredient
from rest_framework.permissions import AllowAny
from .services import IngredientService
from common.views import ServiceModelViewSet
from rest_framework.response import Response

class IngredientViewSet(ServiceModelViewSet):
    
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    service_class = IngredientService
    permission_classes = (AllowAny,)
    
    def list(self, request):
        
        # GET /object
        kwargs = { "user": request.user } if self.filter_by_user else {}
        service = self.service_class()
        objects = service.get_list(params=request.query_params, **kwargs)
        queryset = self.filter_queryset(objects)
        page = self.paginate_queryset(queryset)
        if page is not None:
            data = service.data(page, many=True)
            return self.get_paginated_response(data)

        return Response(service.data(queryset, many=True))
