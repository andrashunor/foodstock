from common.services import ServiceBaseClass
from .dal import ImageDAL

class ImageService(ServiceBaseClass):
    cache = []
    dal_class = ImageDAL
    dal = None
    
    """ Return cached object """
    @classmethod
    def __getCache(cls):
        for o in ImageService.cache:
            return o
        return None
    
    """ Initilize the class and start processing """
    def __new__(cls):
        o = cls.__getCache()
        if o:
            return o
        imageservice = super(ImageService, cls).__new__(cls)
        imageservice.dal = cls.dal_class()
        cls.cache.append(imageservice)
        return imageservice
    
    def get_list(self, **kwargs):
        
        ''' Return Image list '''
        return super().get_list(**kwargs)
    
    def create_object(self, data, **kwargs):
          
        ''' Create and return Image'''
        new_object = super().create_object(data, **kwargs)
        if 'foods' in data:
            new_object = self.dal_class().attach_foods(new_object, data['foods'])
        return new_object
    
    def get_object(self, pk=None, **kwargs):
         
        ''' Return Image for pk '''
        return super().get_object(pk, **kwargs)