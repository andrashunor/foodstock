from django.contrib.auth.models import User
from .models import Food
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')
        

class FoodListSerializer(serializers.ListSerializer):
    class Meta:
        read_only_fields = ('user', )
    
    def validate(self, data):
        """
        Batch foods creation validation
        """
        
        # Get authenticated user 
        names = []
        for food in data:
            food_name = food["name"]
            if food_name in names:
                raise serializers.ValidationError({"message": "Duplicate names are forbidden. Name \"{}\" appears twice in request".format(food_name)})
            names.append(food_name)
        return data
        

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ('name', 'date_modified', 'is_on_stock', 'user', "id", "description")
        extra_kwargs = {'description': {'required': True}}
        read_only_fields = ('user', )
        list_serializer_class = FoodListSerializer
        
        
    def validate(self, data):
        """
        Single food creation validation
        """
                
        # Get authenticated user
        user = self.context['request'].user
        
        name = data.get("name", "")
        if name:
            duplicate_food = Food.objects.filter(user=user, name=name).first()
            if duplicate_food:
                raise serializers.ValidationError({"message": "User already has food named \"{}\"".format(duplicate_food.name)})
        return data        
  
        
class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)
