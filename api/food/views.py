from rest_framework.response import Response
from rest_framework.views import status

from .models import Food
from .serializers import FoodSerializer
from rest_framework.permissions import IsAuthenticated
from .services import FoodService
from common.views import ServiceModelViewSet
    
class FoodViewSet(ServiceModelViewSet):
    
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
    service_class = FoodService
    filter_by_user = True
    permission_classes = (IsAuthenticated,)
    
    """
    Endpoints
    """
        
    def delete_all(self, request):
        
        # GET /food?clear=true
        service = FoodService()
        result = service.clear_food_list(params=self.request.query_params, user=self.request.user)
        if isinstance(result, Exception):
            return Response(result.args[0], status=result.args[1])
        return Response(status=status.HTTP_204_NO_CONTENT)
    
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

