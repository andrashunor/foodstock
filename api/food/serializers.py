from .models import Food
from rest_framework import serializers
from rest_framework.exceptions import NotFound 

class FoodListSerializer(serializers.ListSerializer):
    class Meta:
        read_only_fields = ('user', )
    
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
    class Meta:
        model = Food
        fields = ('name', 'date_modified', 'is_on_stock', 'user', "id", "description")
        extra_kwargs = {'description': {'required': True}}
        read_only_fields = ('user', )
        list_serializer_class = FoodListSerializer
        
    def create(self, validated_data):
        """
        Override default create method
        """
        
        # Add user to data from context
        validated_data['user'] = self.context['user']
        return serializers.ModelSerializer.create(self, validated_data)
        
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
  
        

    
