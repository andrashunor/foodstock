from .models import Food, Recipe
from rest_framework import serializers
from rest_framework.exceptions import NotFound 
from django.utils.functional import empty
from api.ingredient.models import Ingredient
from rest_framework.validators import UniqueTogetherValidator    

class RecipeSerializer(serializers.ModelSerializer):
    
    food = serializers.PrimaryKeyRelatedField(many=False, queryset=Food.objects.all())
    ingredient = serializers.PrimaryKeyRelatedField(many=False, queryset=Ingredient.objects.all())
    
    class Meta:
        model = Recipe
        fields = ('ingredient', 'food', 'amount')
        validators = [
            UniqueTogetherValidator(
                queryset=Recipe.objects.all(),
                fields=('food', 'ingredient')
            )
        ]
        
    @staticmethod
    def serializer_for_data(data=empty, new_object=None):
        
        ''' Create a recipe serializer instance if the data includes recipes '''
        if not 'recipes' in data:
            return None
        recipes_list = data['recipes']
        for elt in recipes_list:
            if isinstance(new_object, Food):
                elt['food'] = new_object.pk
            elif isinstance(new_object, Ingredient):
                elt['ingredient'] = new_object.pk
        
        recipes_list = RecipeSerializer.remove_duplicates(recipes_list)
        return RecipeSerializer(data=recipes_list, many=True)
    
    @staticmethod
    def remove_duplicates(data=empty):
        
        ''' Remove duplicate data based on unique fields, if duplicate data is posted only the first will be used '''
        
        # Beware this is smelly code, try to refactor later
        recipes = []
        for recipe in data:
            recipe_unique = (recipe["food"], recipe["ingredient"])
            if recipe_unique in recipes:
                data.remove(recipe)
            else:
                recipes.append(recipe_unique)
        return data

class FoodListSerializer(serializers.ListSerializer):
    class Meta:
        read_only_fields = ('user', 'recipes')
    
    def validate(self, data):
        """
        List foods validation
        """
        
        # Get authenticated user 
        names = []
        for food in data:
            food_name = food["name"]
            if food_name in names:
                raise serializers.ValidationError({"message": "Duplicate names are forbidden. Name \"{}\" appears twice in request".format(food_name)})
            names.append(food_name)
        return data
    
    def update(self, ids_set, validated_data):
        """
        Update for list is ambiguous.
        Custom logic is implemented here where ids are matched with data and only existing objects are updated
        """
        
        updated_foods = []
        valid_serializers = []
        
        # Check if all objects exist and all data is valid
        for idx, object_id in enumerate(ids_set):
            try:
                food = Food.objects.get(pk=object_id)
                object_data = validated_data[idx]
                update_serializer = FoodSerializer(food, data=object_data, context=self.context, partial=self.partial)
                update_serializer.is_valid(raise_exception=True)
                valid_serializers.append(update_serializer)
            except Food.DoesNotExist:
                raise NotFound({"message": "Food with id: {} does not exist".format(object_id)})
        
        # If all serializers are valid update the objects
        for serializer in valid_serializers:
            serializer.save()
            updated_foods.append(serializer.instance)

        return updated_foods

class FoodSerializer(serializers.ModelSerializer):
    
    recipes = RecipeSerializer(source='recipe_set', many=True, read_only=True)
    user = serializers.ReadOnlyField(source='user.id')
    
    class Meta:
        model = Food
        fields = ('name', 'date_modified', 'is_on_stock', 'user', 'id', 'description', 'image', 'recipes')
        extra_kwargs = {
            'description': {'required': True}, 
        }
        read_only_fields = ('user', 'recipes')
        list_serializer_class = FoodListSerializer
        
    def create(self, validated_data):
        """
        Override default create method
        """
        
        # Add user to data from context
        validated_data['user'] = self.context['user']
        new_object = serializers.ModelSerializer.create(self, validated_data)
        serializer = RecipeSerializer.serializer_for_data(self.initial_data, new_object)
        if serializer:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return new_object
        
    def validate(self, data):
        """
        Single food creation validation
        """
                  
        # Get authenticated user
        user = self.context['user']
        name = data.get("name", "")
        if name:
            duplicate_food = Food.objects.filter(user=user, name=name).first()
            if duplicate_food:
                raise serializers.ValidationError({"message": "User already has food named \"{}\"".format(duplicate_food.name)})
        return data
