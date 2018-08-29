from rest_framework.response import Response
from rest_framework.views import status


def validate_request_data(fn):
    def decorated(*args, **kwargs):
        
        # Not particularly useful at this point. Will keep just to provide example
        # args[0] == GenericView Object
        name = args[0].request.data.get("name", "")
        if not name:
            return Response(
                data={
                    "message": "Food name is required to update food"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)
    return decorated
