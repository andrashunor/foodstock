from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from api.image.models import Image
from api.ingredient.models import Ingredient

class Food(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True, related_name='foods')
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, null=False, blank=True)
    date_modified = models.DateTimeField(default=timezone.now)
    is_on_stock = models.BooleanField(default=False)
    recipes = models.ManyToManyField(
        Ingredient,
        through='Recipe',
        through_fields=('food', 'ingredient'),
    )
#     
    class Meta:
        unique_together = ('user', 'name')

    def __str__(self):
        return self.name
    
class Recipe(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField()


