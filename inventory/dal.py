from rest_framework.serializers import ModelSerializer
from inventory.serializers import FoodSerializer
from .models import Food
from rest_framework.fields import empty

class BaseDataAccessLayer(object):
    serializer_class = ModelSerializer
    model = None
    
    def get_queryset(self):
        return self.model.objects.all()
    
    def get_list(self, **kwargs):
        return self.get_queryset(**kwargs)
    
    def get_object(self, pk=None, **kwargs):
        return self.get_queryset(**kwargs).get_object(pk)
    
    def update_object(self, data, partial=False, **kwargs):
        return self.get_queryset(**kwargs).update_object(data, partial)
    
    def create_object(self, data, **kwargs):
        serializer = self.get_serializer(data=data, **kwargs)
        serializer.is_valid(raise_exception=True)
        return serializer.create(serializer.validated_data)
    
    def delete_object(self, pk, **kwargs):
        self.get_object(pk, **kwargs)
        return self.dal.delete_object(pk)
    
    def data(self, instance, many=False):
        return self.serializer_class(instance, many=many).data
    
    def get_serializer(self, instance=None, data=empty, *args, **kwargs):
        return self.serializer_class(instance, data, *args, **kwargs)

class FoodDAL(BaseDataAccessLayer):
    serializer_class = FoodSerializer
    model = Food
    
    def __init__(self, *args, **kwargs):
        BaseDataAccessLayer.__init__(self, *args, **kwargs)
    
    def get_queryset(self, *args, **kwargs):
        
        ''' Check for user object in kwargs and filter Foods for user '''
        user = self.authenticated_user(**kwargs)
        if user is None:
            return self.model.objects.none()
        return self.model.objects.filter(user=user)
    
    def get_serializer(self, instance=None, data=empty, *args, **kwargs):
        
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        user = self.authenticated_user(**kwargs)
        kwargs = {'context':{'user':user}}
        return self.serializer_class(instance=instance, data=data, **kwargs)
    
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

    