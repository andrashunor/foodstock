from common.services import ServiceBaseClass
from .dal import IngredientDAL

class IngredientService(ServiceBaseClass):
    cache = []
    dal_class = IngredientDAL
    dal = None
    
    """ Return cached object """
    @classmethod
    def __getCache(cls):
        for o in IngredientService.cache:
            return o
        return None
    
    """ Initilize the class and start processing """
    def __new__(cls):
        o = cls.__getCache()
        if o:
            return o
        service = super(IngredientService, cls).__new__(cls)
        service.dal = cls.dal_class()
        cls.cache.append(service)
        return service