from rest_framework.response import Response
from rest_framework.views import status
from .models import Food
import re

# This class is not used currently in the project. Nonetheless is kept to provide useful example
# Methods can be called by e.g. @validate_food_name in views

def validate_food_name(fn):
    def decorated(*args, **kwargs):
        
        # args[0] == GenericView Object
        name = args[0].request.data.get("name", "")
        if name:
            user = args[0].request.user
            if Food.objects.filter(user=user, name=name).count() > 0:
                return Response(
                    data={
                        "message": "Food name for user already exists"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        return fn(*args, **kwargs)
    return decorated

def validate_food_names(fn):
    def decorated(*args, **kwargs):
        
        # args[0] == GenericView Object
        data = args[0].request.data
        if isinstance(data, list):
            user = args[0].request.user
            names = []
            for food in data:
                food_name = food["name"]
                if food_name in names:
                    return Response(
                        data={
                            "message": "Duplicate names are forbidden. Name \"" + food_name + "\" appears twice in request"
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                names.append(food_name)
            duplicate_food = Food.objects.filter(user=user, name__in=names).first()
            if duplicate_food:
                return Response(
                    data={
                        "message": "Food called " + duplicate_food.name + " already exists"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        return fn(*args, **kwargs)
    return decorated

def validate_for_list_update(fn):
    def decorated(*args, **kwargs):
        
        # args[0] == GenericView Object
        request = args[0].request
        if not 'many' in request.query_params or not 'ids' in request.query_params:
            
            # request URL does not include necessary params
            return Response(data={"message": "Missing parameters. Must contain \"many\" and \"ids\""}, status=status.HTTP_400_BAD_REQUEST)
        
        if not request.query_params["many"]:
            
            # many param is not True
            return Response(data={"message": "\"many\" should be True"}, status=status.HTTP_400_BAD_REQUEST)
            
        ids_str = request.query_params['ids']
        if not re.match("\d+(?:,\d+)?", ids_str):
            
            # unauthorized characters
            return Response(data={"message": "Unauthorized characters in \"ids\" parameter. Correct format is numbers separated by \",\" characters."}, status=status.HTTP_400_BAD_REQUEST)
        
        ids = ids_str.split(',')
        
        if not isinstance(ids, list):
        
            # ids param not a list
            return Response(data={"message": "Format error. \"ids\" should be a list."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not isinstance(request.data, list) or len(ids) != len(request.data):
            
            # mismatch between ids param and request data
            return Response(data={"message": "\"ids\" param length did not match request.data length"}, status=status.HTTP_400_BAD_REQUEST)
        return fn(*args, **kwargs)
    return decorated
