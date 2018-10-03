from django.db import models
from django.db.models.fields.files import ImageField

class Image(models.Model):
    image = ImageField(upload_to='images/')
    description = models.CharField(max_length=100, default="", null=True, blank=True)