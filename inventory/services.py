from .managers import FoodQuerySet

class ServiceBaseClass(object):
    queryset = None
    
    def get_list(self, pagination=False, **filters):
        return self.queryset.filter(**filters)

class FoodService(ServiceBaseClass):
        
    def __init__(self, user=None, *args, **kwargs):
        ServiceBaseClass.__init__(self, *args, **kwargs)
        self.queryset = FoodQuerySet()
        self.queryset.user = user
    
    def get_foods(self, pagination=False, **filters):
        
        ''' Return Food list'''
        return self.get_list(pagination)
        
#     def update_food_list(self, data, partial=False):
#          
#         ''' Update and return food list '''
#          
#     def clear_food_list(self):
#          
#         ''' Clear all foods for user return is_successful '''
#          
#     def update_food(self, pk, data, partial=False):
#          
#         ''' Update and return Food '''
#         return Food.objects.get(pk=pk)
#      
#     def create_food(self, pk, data):
#          
#         ''' Create and return Food'''
#     
    def get_food(self, pk=None):
         
        ''' Return Food for pk '''
        FoodQuerySet().get_object(pk)

# #         
#     def delete_food(self, pk):
#          
#         ''' Delete food return is_successful '''

