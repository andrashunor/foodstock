from api.ingredient.models import Ingredient
from rest_framework import serializers
from api.food.serializers import RecipeSerializer

class IngredientSerializer(serializers.ModelSerializer):
    
    recipes = RecipeSerializer(source='recipe_set', many=True, read_only=True)
        
    class Meta:
        model = Ingredient
        fields = ('name', 'is_on_stock', 'id', 'description', 'image', 'recipes')
        read_only_fields = ('recipes', )

    def create(self, validated_data):
        """
        Override default create method
        """
        
        # Add user to data from context
        new_object = serializers.ModelSerializer.create(self, validated_data)
        serializer = RecipeSerializer.serializer_for_data(self.initial_data, new_object)
        if serializer:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return new_object    
