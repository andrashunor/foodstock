from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Food
from .serializers import FoodSerializer
from django.contrib.auth.models import User

class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_food(user=User(), name=""):
        if user != None and name != "":
            Food.objects.create(user=user, name=name)

    def setUp(self):
        # add test data
        superuser = User.objects.create_superuser('superuser', 'a@a.com', 'password')
        self.assertIsNotNone(superuser, 'Superuser should exist')
        self.create_food(superuser, "Tomato")
        self.create_food(superuser, "Ham")
        self.create_food(superuser, "Eggs")
        self.create_food(superuser, "Butter")
        
        
class GetAllFoodsTest(BaseViewTest):
  
    def test_get_all_foods(self):
          
        """
        This test ensures that all songs added in the setUp method
        exist when we make a GET request to the songs/ endpoint
        """
        # hit the API endpoint
        response = self.client.get(
            reverse("foods-all")
        )
        # fetch the data from db
        expected = Food.objects.all()
        serialized = FoodSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)