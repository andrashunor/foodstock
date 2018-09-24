from .dal import FoodDAL, BaseDataAccessLayer

class ServiceBaseClass(object):
    dal_class = BaseDataAccessLayer
    dal = None
    
    def get_list(self, **kwargs):
        return self.dal.get_list(**kwargs)
    
    def get_object(self, pk=None, **kwargs):
        return self.dal.get_object(pk)
    
    def update_object(self, data, partial=False, **kwargs):
        return self.dal.update_object(data, partial)
    
    def create_object(self, data, **kwargs):
        return self.dal.create_object(data, **kwargs)
    
    def delete_object(self, pk, **kwargs):
        return self.dal.delete_object(pk)
    
    def data(self, instance, many=False):
        return self.dal.data(instance, many)

class FoodService(ServiceBaseClass):
    dal_class = FoodDAL
    dal = None
    
    def __init__(self):
        ServiceBaseClass.__init__(self)
        self.dal = self.dal_class()
    
    def get_foods(self, **kwargs):
        
        ''' Return Food list '''
        return super().get_list(**kwargs)
        
    def update_food_list(self, data, partial=False, **kwargs):
          
        ''' Update and return food list '''
        return super().update_food_list(data, partial, **kwargs)
          
    def clear_food_list(self, **kwargs):
          
        ''' Clear all foods for user return is_successful '''
          
    def update_food(self, pk, data, partial=False, **kwargs):
          
        ''' Update and return Food '''
        return super().update_food(pk, data, partial, **kwargs)
      
    def create_food(self, data, **kwargs):
          
        ''' Create and return Food'''
        return super().create_object(data, **kwargs)
     
    def get_food(self, pk=None, **kwargs):
         
        ''' Return Food for pk '''
        return super().get_food(pk, **kwargs)
         
    def delete_food(self, pk, **kwargs):
          
        ''' Delete food return is_successful '''
        return super().delete_food(pk, **kwargs)
        
    def data(self, instance, many=False):
        
        ''' Data for instance '''
        return super().data(instance, many)

