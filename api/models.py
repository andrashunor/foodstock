from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.fields.files import ImageField

class Image(models.Model):
    image = ImageField()
    description = models.CharField(max_length=100, default="", null=True, blank=True)

class Food(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, null=False, blank=True)
    date_modified = models.DateTimeField(default=timezone.now)
    is_on_stock = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('user', 'name')

    def __str__(self):
        return self.name

