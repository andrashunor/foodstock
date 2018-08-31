from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Food(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    date_modified = models.DateTimeField(default=timezone.now)
    is_on_stock = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('user', 'name')

    def __str__(self):
        return self.name