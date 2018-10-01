from rest_framework import serializers
from .models import Image

class ImageSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id'
    )

    class Meta:
        model = Image
        fields = '__all__'
        read_only_fields = ('image', 'description')
    