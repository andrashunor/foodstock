from .serializers import IngredientSerializer
from .models import Ingredient
from common.dal import BaseDataAccessLayer

class IngredientDAL(BaseDataAccessLayer):
    cache = []
    serializer_class = IngredientSerializer
    model = Ingredient
    
    """ Return cached object """
    @classmethod
    def __getCache(cls):
        for o in IngredientDAL.cache:
            return o
        return None
    
    """ Initilize the class and start processing """
    def __new__(cls):
        o = cls.__getCache()
        if o:
            return o
        dal = super(IngredientDAL, cls).__new__(cls)
        cls.cache.append(dal)
        return dal