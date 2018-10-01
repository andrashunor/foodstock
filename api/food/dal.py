from .serializers import FoodSerializer
from .models import Food
from rest_framework.fields import empty
from common.dal import BaseDataAccessLayer

class FoodDAL(BaseDataAccessLayer):
    cache = []
    serializer_class = FoodSerializer
    model = Food
    
    """ Return cached object """
    @classmethod
    def __getCache(cls):
        for o in FoodDAL.cache:
            return o
        return None
    
    """ Initilize the class and start processing """
    def __new__(cls):
        o = cls.__getCache()
        if o:
            return o
        food_dal = super(FoodDAL, cls).__new__(cls)
        cls.cache.append(food_dal)
        return food_dal
    
    def __init__(self, *args, **kwargs):
        BaseDataAccessLayer.__init__(self, *args, **kwargs)
    
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
    