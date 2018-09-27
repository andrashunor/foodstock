from .services import ServiceBaseClass
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.serializers import ModelSerializer

class ServiceModelViewSet(ModelViewSet):
    
    """
    ServiceViewSet for Object model
    GET object
    POST object
    DELETE object
    PUT object
    GET object/:id
    PUT object/:id
    PATCH object/:id
    DELETE object/:id
    """
    
    serializer_class = ModelSerializer
    service_class = ServiceBaseClass
    filter_by_user = False
    
    """
    Endpoints
    """
    
    def list(self, request):
        
        # GET /object
        kwargs = { "user": request.user } if self.filter_by_user else {}
        service = self.service_class()
        objects = service.get_list(**kwargs)
        queryset = self.filter_queryset(objects)
        page = self.paginate_queryset(queryset)
        if page is not None:
            data = service.data(page, many=True)
            return self.get_paginated_response(data)

        return Response(service.data(queryset, many=True))

    def create(self, request):
        
        # POST /object
        kwargs = { "user": request.user } if self.filter_by_user else {}
        many = isinstance(request.data, list)
        service = self.service_class()
        new_object = service.create_object(request.data, **kwargs)
        return Response(data=service.data(new_object, many=many), status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        
        # GET /object/:id
        kwargs = { "user": request.user } if self.filter_by_user else {}
        service = self.service_class()
        result = service.get_object(pk, **kwargs)
        if isinstance(result, Exception):
            return Response(result.args[0], status=result.args[1])
        return Response(service.data(result), status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        
        # PUT /object/:id
        kwargs = { "user": request.user } if self.filter_by_user else {}
        service = self.service_class()
        result = service.update_object(pk, data=request.data, **kwargs)
        if isinstance(result, Exception):
            return Response(result.args[0], status=result.args[1])
        return Response(service.data(result), status=status.HTTP_200_OK)
        
    def partial_update(self, request, pk=None):
        
        # PATCH /object/:id
        kwargs = { "user": request.user } if self.filter_by_user else {}
        service = self.service_class()
        result = service.update_object(pk, data=request.data, partial=True, **kwargs)
        if isinstance(result, Exception):
            return Response(result.args[0], status=result.args[1])
        return Response(service.data(result), status=status.HTTP_200_OK)
    
    def destroy(self, request, pk=None):
        
        # DELETE /object/:id
        kwargs = { "user": request.user } if self.filter_by_user else {}
        service = self.service_class()
        result = service.delete_object(pk, **kwargs)
        if isinstance(result, Exception):
            return Response(result.args[0], status=result.args[1])
        return Response(status=status.HTTP_204_NO_CONTENT)

