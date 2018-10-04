from api.ingredient.models import Ingredient
from api.food.models import Food
from rest_framework import serializers


class IngredientSerializer(serializers.ModelSerializer):
    
    ''' Set up relationship between models where objects are referred by their pk.  e.g. foods: [1, 2, 3] in body will attach foods to ingredient if they exist '''
    foods = serializers.PrimaryKeyRelatedField(many=True, queryset=Food.objects.all(), required=False)

    class Meta:
        model = Ingredient
        fields = ('name', 'is_on_stock', 'foods', 'id', 'description', 'image')
