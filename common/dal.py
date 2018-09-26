from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.serializers import ModelSerializer
from rest_framework.fields import empty

class BaseDataAccessLayer(object):
    cache = []
    serializer_class = ModelSerializer
    model = None
    
    def get_queryset(self):
        
        """ Default queryset """
        return self.model.objects.all()
    
    def get_list(self, **kwargs):
        
        """ Returns a list of model object filtered by kwargs """
        return self.get_queryset(**kwargs)
    
    def get_object(self, pk=None, **kwargs):
        
        """ Return instance of model object or exception """
        try:
            return self.get_queryset(**kwargs).get(pk=pk)
        except self.model.DoesNotExist:

            # Send back default not found response
            return ObjectDoesNotExist({"message": "{} with id: {} does not exist".format(self.model._meta.object_name, pk)}, status.HTTP_404_NOT_FOUND)
        
    def create_object(self, data, **kwargs):
        
        """ Validates data, creates object, returns instance or exception """
        serializer = self.get_serializer(data=data, **kwargs)
        serializer.is_valid(raise_exception=True)
        return serializer.create(serializer.validated_data)
    
    def update_object(self, pk, data, partial=False, **kwargs):
        
        """ Validates data, updates object, returns instance or exception """
        result = self.get_object(pk, **kwargs)
        if not isinstance(result, self.model):
            
            # Return exception
            return result
        
        # Update and return instance
        serializer = self.get_serializer(instance=result, data=data, partial=partial, **kwargs)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.instance
    
    def delete_object(self, pk, **kwargs):
        
        """ Delete object, return None or exception """
        result = self.get_object(pk, **kwargs)
        if not isinstance(result, self.model):
                    
            # Return exception
            return result
        
        # Delete object
        result.delete()
        return None

    
    def data(self, instance, many=False):
        
        """ Return json representation of the object instance(s) """
        return self.serializer_class(instance, many=many).data
    
    def get_serializer(self, instance=None, data=empty, *args, **kwargs):
        
        """ Get instance of the serializer class """
        return self.serializer_class(instance, data, *args, **kwargs)
