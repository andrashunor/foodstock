from .serializers import ImageSerializer
from .models import Image
from rest_framework.fields import empty
from common.dal import BaseDataAccessLayer
from api.food.services import FoodService

class ImageDAL(BaseDataAccessLayer):
    cache = []
    serializer_class = ImageSerializer
    model = Image
    
    """ Return cached object """
    @classmethod
    def __getCache(cls):
        for o in ImageDAL.cache:
            return o
        return None
    
    """ Initilize the class and start processing """
    def __new__(cls):
        o = cls.__getCache()
        if o:
            return o
        image_dal = super(ImageDAL, cls).__new__(cls)
        cls.cache.append(image_dal)
        return image_dal
    
    def get_serializer(self, instance=None, data=empty, partial=False, *args, **kwargs):
        
        """
        Get instance of the ImageSerializer class with user in context
        """
        many = isinstance(data, list)
        return self.serializer_class(instance=instance, data=data, many=many, partial=partial, **kwargs)
    
    def attach_foods(self, image=Image, foods=None):
        if foods is None:
            return image
        ids = foods.split(',')
        key = 'pk__in' if isinstance(ids, list) else 'pk'
        kwargs = {key: ids}
        service = FoodService()
        foods = service.get_list(**kwargs)
        for food in foods:
            image.foods.add(food)
        return image
