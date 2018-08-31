from rest_framework.response import Response
from rest_framework.views import status
from .models import Food


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
