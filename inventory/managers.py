from django.core.exceptions import ObjectDoesNotExist
from inventory.serializers import FoodListSerializer
from .models import Food
from django.db import models


class BaseQuerySet(models.QuerySet):
    serializer_class = None
    
    def get_object(self, pk=None):
        try:
            an_object = self.get(pk=pk)
            return an_object
        except self.model.DoesNotExist:

            # Send back default not found response
            return ObjectDoesNotExist({"message": "{} with id: {} does not exist".format(self.model._meta.object_name, pk)})
        
    def get_object_data(self, pk=None):
        result = self.get_object(pk=1)
        if isinstance(result, Exception):
            return result
        
        return self.serializer_class(result).data
        
        
    @property
    def data(self):
        
        ''' Use the Serializer class here to return data representation of self '''
        serializer = self.serializer_class(self, many=True)
        print(serializer)
        return serializer.data
    
class FoodQuerySet(BaseQuerySet):
    model = Food
    serializer_class = FoodListSerializer
    user = None
    
    def foods(self, user=None):
        if user is None:
            user = self.user
            
        if user.is_anonymous:
            return self.model.objects.none()
        return self.model.objects.filter(user=user)