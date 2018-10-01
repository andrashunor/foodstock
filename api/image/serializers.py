from rest_framework import serializers
from .models import Image
from api.food.serializers import FoodSerializer

class ImageSerializer(serializers.HyperlinkedModelSerializer):
    foods = FoodSerializer(many=True, read_only=True)

    class Meta:
        model = Image
        fields = ('image', 'description', 'id', 'foods')
        read_only_fields = ('foods', )
