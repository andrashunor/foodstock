from rest_framework.viewsets import ModelViewSet
from .serializers import ImageSerializer
from .models import Image
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from .services import ImageService
from rest_framework.views import status
from rest_framework.response import Response

class ImageViewSet(ModelViewSet):
    
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    service_class = ImageService
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        service = self.service_class()
        new_object = service.create_object(request.data, context=self.get_serializer_context())
        return Response(data=self.get_serializer(new_object).data, status=status.HTTP_201_CREATED)
