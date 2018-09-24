from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

class BaseQuerySet(models.Manager):
    serializer_class = None
    
    def get_object(self, pk=None):
        try:
            an_object = self.get(pk=pk)
            return an_object
        except self.model.DoesNotExist:

            # Send back default not found response
            return ObjectDoesNotExist({"message": "{} with id: {} does not exist".format(self.model._meta.object_name, pk)})
        
    def get_object_data(self, pk=None):
        result = self.get_object(pk=1)
        if isinstance(result, Exception):
            return result
        
        return self.serializer_class(result).data
    
class FoodQuerySet(BaseQuerySet):
    user = None
    
    def foods(self, user=None):
        if user is None:
            user = self.user
            
        if user.is_anonymous:
            return self.model.objects.none()
        return self.model.objects.filter(user=user)

class Food(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, null=False, blank=True)
    date_modified = models.DateTimeField(default=timezone.now)
    is_on_stock = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('user', 'name')

    def __str__(self):
        return self.name
    