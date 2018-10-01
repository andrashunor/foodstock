from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.views import status
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Image

class FileUploadTests(APITestCase):
    client = APIClient()
    
    def setUp(self):
        self.tearDown()
        u = User.objects.create_user('test', password='test', email='test@test.test')
        self.client.force_authenticate(u)

    def _create_test_file(self, path):

        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded = SimpleUploadedFile('small.gif', small_gif, content_type='image/gif')
        return {'image': uploaded}

    def test_upload_file(self):
        url = reverse('image-list')
        data = self._create_test_file('/tmp/test_upload')

        images = Image.objects.all()
        response = self.client.post(url, data, format='multipart')
        test_against = Image.objects.all()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(images, test_against, 'The two sets should be different')