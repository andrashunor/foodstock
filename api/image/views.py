from rest_framework.viewsets import ModelViewSet
from .serializers import ImageSerializer
from .models import Image
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated

class ImageViewSet(ModelViewSet):
    
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(description=self.request.data.get('description'), image=self.request.data.get('image'))