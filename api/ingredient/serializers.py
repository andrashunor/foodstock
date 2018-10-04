from api.ingredient.models import Ingredient
from rest_framework import serializers


class IngredientSerializer(serializers.ModelSerializer):
    foods = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Ingredient
        fields = ('name', 'is_on_stock', 'foods', 'id', 'description', 'image')
