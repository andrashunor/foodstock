from django.db import models
from api.image.models import Image
from api.food.models import Food

class Ingredient(models.Model):
    foods = models.ManyToManyField(Food, related_name='ingredients')
    image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True, related_name='ingredients')
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100, null=False, blank=True)
    is_on_stock = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
