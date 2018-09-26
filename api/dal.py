from rest_framework.serializers import ModelSerializer
from .serializers import FoodSerializer
from .models import Food
from rest_framework.fields import empty
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

class BaseDataAccessLayer(object):
    cache = []
    serializer_class = ModelSerializer
    model = None

    """ Return cached object """
    @classmethod
    def __getCache(cls):
        for o in BaseDataAccessLayer.cache:
            return o
        return None
    
    """ Initilize the class and start processing """
    def __new__(cls):
        o = cls.__getCache()
        if o:
            return o
        foodservice = super(BaseDataAccessLayer, cls).__new__(cls)
        cls.cache.append(foodservice)
        return foodservice
    
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

class FoodDAL(BaseDataAccessLayer):
    serializer_class = FoodSerializer
    model = Food
    
    def __init__(self, *args, **kwargs):
        BaseDataAccessLayer.__init__(self, *args, **kwargs)
    
    def get_queryset(self, *args, **kwargs):
        
        """ Check for user object in kwargs and filter Foods for user """
        user = self.authenticated_user(**kwargs)
        if user is None:
            return self.model.objects.none()
        return self.model.objects.filter(user=user)
    
    def get_serializer(self, instance=None, data=empty, partial=False, *args, **kwargs):
        
        """
        Get instance of the FoodSerializer class with user in context
        """
        user = self.authenticated_user(**kwargs)
        kwargs = {'context':{'user':user}}
        many = isinstance(data, list)
        return self.serializer_class(instance=instance, data=data, many=many, partial=partial, **kwargs)
    
    def authenticated_user(self, **kwargs):
        
        """ Extract user from kwargs """
        if not 'user' in kwargs:
            return None
        user = kwargs['user']
        if user is None:
            return None
        if user.is_anonymous:
            return None
        return user
    
    def clear_food_list(self, **kwargs):
        self.get_list(**kwargs).delete()
        
    def update_food_list(self, ids=None, data=None, partial=False, **kwargs):
        serializer = self.get_serializer(data=data, many=True, partial=partial, **kwargs)
        serializer.is_valid(raise_exception=True)
        updated_objects = serializer.update(ids, data)
        return updated_objects
    