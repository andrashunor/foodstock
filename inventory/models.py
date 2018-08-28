from django.db import models
from django.contrib.auth.models import User


class Food(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    date_modified = models.DateTimeField('date modified')
    is_on_stock = models.BooleanField()
    def __str__(self):
        return self.name