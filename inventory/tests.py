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
        self.user = User.objects.create_user('user', 'a@a.com', 'password')
        self.assertIsNotNone(self.user, 'user should exist')
        self.create_food(self.user, "Tomato")
        self.create_food(self.user, "Ham")
        self.create_food(self.user, "Eggs")
        self.create_food(self.user, "Butter")
        
class AuthenticatedViewTest(APITestCase):
    client = APIClient()
        
    def setUp(self):
        
        # add test data
        self.user = User.objects.create_user('authuser', 'a@b.com', 'password')
        self.client.force_authenticate(self.user)
        
class AllFoodsTest(BaseViewTest):
  
    def test_get_all_foods(self):
          
        """
        This test ensures that all foods added in the setUp method
        exist when we make a GET request to the foods/ endpoint
        """
        
        # hit the API endpoint
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse("foods"))
        
        # fetch the data from db
        expected = Food.objects.all()
        serialized = FoodSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_no_foods(self):
        
        """
        This test ensures that no foods added in the setUp method
        can be accessed by unauthorized user when we make a GET request to the foods/ endpoint
        """
        
        # hit the API endpoint
        no_foods_user = User.objects.create_user('no_food_user', 'a@b.com', 'password')
        self.client.force_authenticate(no_foods_user)
        response = self.client.get(reverse("foods"))
        
        # fetch the data from db
        expected = Food.objects.filter(user=no_foods_user)
        serialized = FoodSerializer(expected, many=True)
        self.assertEqual(response.data, [], 'Response data should be empty')
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_delete_all_foods(self):
        
        """
        This test ensures that no foods added in the setUp method
        can be deleted by the foods-clear/ endpoint
        """
                
        # fetch the data from db
        foods = Food.objects.filter(user=self.user)
        self.assertNotEqual(foods.count(), 0, 'Foods should not be 0')

        # hit the API endpoint
        self.client.force_authenticate(self.user)
        response = self.client.delete(reverse("foods-clear"))
        
        # fetch the data from db
        expected = Food.objects.filter(user=self.user)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(expected.count(), 0, 'Foods count should be 0')
    
class LoginTest(BaseViewTest):
     
    def test_login(self):
         
        """
        This test ensures that the we can log in with user created in setUp
        """
        
        client = APIClient()
        is_successful = client.login(username='user', password='password')
        self.assertTrue(is_successful, 'Login should be successful')
        
    
class FoodCRUDTest(AuthenticatedViewTest):
    
    def test_create_food(self):
        
        """
        This test ensures that food can be created when we make POST call to the foods/ endpoint
        """
        
        # hit the API endpoint
        response = self.client.post(reverse('foods'), {"name": "tomato"})
        
        # check response
        food = FoodSerializer(data=response.data)
        self.assertIsNotNone(food, 'Food from data should exist')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                
    def test_update_food(self):
        
        """
        This test ensures that food gets updated when we make PUT call to the food-detail/ endpoint
        """
        new_name = 'new_name'
        food = Food.objects.create(user=self.user, name='old_name')
        
        # hit the API endpoint
        response = self.client.put(reverse('food-detail', kwargs={'pk': food.id}), {"name": 'new_name'})
        
        # check response
        self.assertEqual(new_name, response.data["name"], 'Name should been updated')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_food(self):
        
        """
        This test ensures that food gets deleted when we make DELETE call to the food-detail/ endpoint
        """
        food = Food.objects.create(user=self.user, name='test')
        
        # hit the API endpoint
        response = self.client.delete(reverse('food-detail', kwargs={'pk': food.id}))
        
        # check response
        self.assertFalse(Food.objects.filter(name='test').exists(), 'Food should no longer exist in the database')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_get_food(self):
        
        """
        This test ensures that food can be fetched when we make GET call to the food-detail/ endpoint
        """
        food = Food.objects.create(user=self.user, name='test')
        
        # hit the API endpoint
        response = self.client.get(reverse('food-detail', kwargs={'pk': food.id}))
        
        # check response
        test_against = FoodSerializer(food).data
        self.assertEqual(response.data, test_against, 'The food data should be equal')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_create_food_batch(self):
        
        """
        This test ensures that multiple foods can be created when we make POST call to the foods-create-batch/ endpoint
        """
        
        # hit the API endpoint
        response = self.client.post(reverse('foods-create-batch'), [{"name": "tomato"}, {"name": "tomato1"}, {"name": "tomato2"}, {"name": "tomato3"}])
        
        expected = Food.objects.filter(user=self.user)
        serialized = FoodSerializer(expected, many=True)
        
        # check response
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_food_name_unique(self):
        
        """
        This test ensures that user is unable to create multiple foods with the same name when making POST call to the foods/ endpoint
        """
        
        # hit the API endpoint
        Food.objects.create(user=self.user, name='tomato')
        response = self.client.post(reverse('foods'), {"name": "tomato"})
        
        # check response
        self.assertIsNotNone(response.data['message'], 'Response should contain error message')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_unauthorized_update(self):
         
        """
        This test ensures that user is unable to update food that was not created by him when making PUT call to the foods/ endpoint
        """
         
        user = User.objects.create_user('username', 'email', 'password')
        food = Food.objects.create(user=user, name='tomato')
         
        # hit the API endpoint
        response = self.client.put(reverse('food-detail', kwargs={'pk': food.id}), {"name": 'new_name'})
         
        # check response
        self.assertIsNotNone(response.data['message'], 'Response should contain error message')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        