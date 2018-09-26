from .dal import FoodDAL
from common.services import ServiceBaseClass
from rest_framework import status
import re

class FoodService(ServiceBaseClass):
    cache = []
    dal_class = FoodDAL
    dal = None
    
    """ Return cached object """
    @classmethod
    def __getCache(cls):
        for o in FoodService.cache:
            return o
        return None
    
    """ Initilize the class and start processing """
    def __new__(cls):
        o = cls.__getCache()
        if o:
            return o
        foodservice = super(FoodService, cls).__new__(cls)
        foodservice.dal = cls.dal_class()
        cls.cache.append(foodservice)
        return foodservice
    
    def get_foods(self, **kwargs):
        
        ''' Return Food list '''
        return super().get_list(**kwargs)
    
    def create_food(self, data, **kwargs):
          
        ''' Create and return Food'''
        return super().create_object(data, **kwargs)
    
    def get_food(self, pk=None, **kwargs):
         
        ''' Return Food for pk '''
        return super().get_object(pk, **kwargs)
          
    def update_food(self, pk, data, partial=False, **kwargs):
          
        ''' Update and return Food '''
        return super().update_object(pk=pk, data=data, partial=partial, **kwargs)
         
    def delete_food(self, pk, **kwargs):
          
        ''' Delete food return is_successful '''
        return super().delete_object(pk, **kwargs)
    
    def update_food_list(self, params=None, data=None, partial=False, **kwargs):
          
        ''' Update and return food list '''
        
        if not 'many' in params or not 'ids' in params:
            
            # request URL does not include necessary params
            return Exception({"message": "Missing parameters. Must contain \"many\" and \"ids\""}, status=status.HTTP_400_BAD_REQUEST)
        
        if not params["many"]:
            
            # many param is not True
            return Exception({"message": "\"many\" should be True"}, status=status.HTTP_400_BAD_REQUEST)
            
        ids_str = params['ids']
        if not re.match("\d+(?:,\d+)?", ids_str):
            
            # unauthorized characters
            return Exception({"message": "Unauthorized characters in \"ids\" parameter. Correct format is numbers separated by \",\" characters."}, status=status.HTTP_400_BAD_REQUEST)
        
        ids = ids_str.split(',')
        
        if not isinstance(ids, list):
        
            # ids param not a list
            return Exception({"message": "Format error. \"ids\" should be a list."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not isinstance(data, list) or len(ids) != len(data):
            
            # mismatch between ids param and request data
            return Exception({"message": "\"ids\" param length did not match request.data length"}, status=status.HTTP_400_BAD_REQUEST)
        
        return self.dal.update_food_list(ids, data, partial, **kwargs)
        
          
    def clear_food_list(self, params=None, **kwargs):
          
        ''' Clear all foods for user '''
        if 'clear' in params:
            if params["clear"]:
                return self.dal.clear_food_list(**kwargs)
        return Exception({"message": "Method not allowed"}, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def data(self, instance, many=False):
        
        ''' Data for instance '''
        return super().data(instance, many)

