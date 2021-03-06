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
            Food.objects.create(user=user, name=name, description="")

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
        exist when we make a GET request to the /food endpoint
        """
        
        # hit the API endpoint
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse("food-list"))
        
        # fetch the data from db
        expected = Food.objects.all()
        serialized = FoodSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_no_foods(self):
        
        """
        This test ensures that no foods added in the setUp method
        can be accessed by unauthorized user when we make a GET request to the /food endpoint
        """
        
        # hit the API endpoint
        no_foods_user = User.objects.create_user('no_food_user', 'a@b.com', 'password')
        self.client.force_authenticate(no_foods_user)
        response = self.client.get(reverse("food-list"))
        
        # fetch the data from db
        expected = Food.objects.filter(user=no_foods_user)
        serialized = FoodSerializer(expected, many=True)
        self.assertEqual(response.data, [], 'Response data should be empty')
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_delete_all_foods(self):
        
        """
        This test ensures that no foods added in the setUp method can be deleted by the /food endpoint
        """
                
        # fetch the data from db
        foods = Food.objects.filter(user=self.user)
        self.assertNotEqual(foods.count(), 0, 'Foods should not be 0')

        # hit the API endpoint
        self.client.force_authenticate(self.user)
        query = "?clear=true"
        response = self.client.delete(reverse("food-list")+query)
        
        # fetch the data from db
        expected = Food.objects.filter(user=self.user)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(expected.count(), 0, 'Foods count should be 0')
        
        
    def test_etag_all_foods(self):
        
        """
        This test ensures that foods are not returned after ETag has been to into the header when we make a get request to the /food endpoint
        """
        
        # hit the API endpoint
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse("food-list"))
        
        # fetch the data from db
        expected = Food.objects.all()
        serialized = FoodSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        header = {"HTTP_IF_NONE_MATCH": response["ETag"] }
        second_response = self.client.get(reverse("food-list"), **header)
        self.assertEqual(second_response.status_code, status.HTTP_304_NOT_MODIFIED, 'Status expectation failed')
    
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
        This test ensures that food can be created when we make POST call to the /food endpoint
        """
        
        # hit the API endpoint
        response = self.client.post(reverse('food-list'), {"name": "tomato", "description": ""})
        
        # check response
        food = FoodSerializer(data=response.data)
        self.assertIsNotNone(food, 'Food from data should exist')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                
    def test_successful_update_food(self):
        
        """
        This test ensures that food gets updated when we make PUT call to the food/:id endpoint
        """
        new_name = 'new_name'
        food = Food.objects.create(user=self.user, name='old_name')
        
        # hit the API endpoint
        response = self.client.put(reverse('food-detail', kwargs={'pk': food.id}), {"name": 'new_name', "description": "new_description"})
        
        # check response
        self.assertEqual(new_name, response.data["name"], 'Name should been updated')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_failed_update_food(self):
        
        """
        This test ensures that food gets updated when we make PUT call to the food/:id endpoint
        """
        new_name = 'new_name'
        food = Food.objects.create(user=self.user, name='old_name')
        
        # hit the API endpoint
        response = self.client.put(reverse('food-detail', kwargs={'pk': food.id}), {"name": new_name})
        
        test_against = Food.objects.get(pk=food.id)
        
        # check response
        self.assertNotEqual(test_against.name, new_name, 'New name should not be saved in the DB')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_partial_update_food(self):
        
        """
        This test ensures that food gets partially updated when we make PATCH call to the food/:id endpoint
        """
        new_name = 'new_name'
        food = Food.objects.create(user=self.user, name='old_name')
        
        # hit the API endpoint
        response = self.client.patch(reverse('food-detail', kwargs={'pk': food.id}), {"name": 'new_name'})
        
        # check response
        self.assertEqual(new_name, response.data["name"], 'Name should been updated')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_food(self):
        
        """
        This test ensures that food gets deleted when we make DELETE call to the food/:id endpoint
        """
        food = Food.objects.create(user=self.user, name='test')
        
        # hit the API endpoint
        response = self.client.delete(reverse('food-detail', kwargs={'pk': food.id}))
        
        # check response
        self.assertFalse(Food.objects.filter(name='test').exists(), 'Food should no longer exist in the database')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_get_food(self):
        
        """
        This test ensures that food can be fetched when we make GET call to the food/:id endpoint
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
        response = self.client.post(reverse('food-list'), [{"name": "tomato", "description": ""}, {"name": "tomato1", "description": ""}, {"name": "tomato2", "description": ""}, {"name": "tomato3", "description": ""}])
        
        expected = Food.objects.filter(user=self.user)
        serialized = FoodSerializer(expected, many=True)
        
        # check response
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_partial_update_food_batch(self):
        
        """
        This test ensures that multiple foods can be updated when we make PATCH call to the foods-list/ endpoint
        """
        
        food = Food.objects.create(user=self.user, name="name", description="")
        food1 = Food.objects.create(user=self.user, name="name1", description="")
        food2 = Food.objects.create(user=self.user, name="name2", description="")
         
        # hit the API endpoint
        query = "?many=true&ids={},{},{}".format(food.id, food1.id,food2.id)
        response = self.client.patch(reverse('food-list')+query, [{"name": "tomato"}, {"name": "tomato1"}, {"name": "tomato2"}])
         
        food_names = [food.name, food1.name, food2.name]
        self.assertFalse(Food.objects.filter(name__in=food_names).exists(), 'Foods with these names should no longer exist')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_food_name_unique(self):
        
        """
        This test ensures that user is unable to create multiple foods with the same name when making POST call to the /food endpoint
        """
        
        # hit the API endpoint
        Food.objects.create(user=self.user, name='tomato', description="")
        response = self.client.post(reverse('food-list'), {"name": "tomato", "description": ""})
        
        # check response
        self.assertIsNotNone(response.data['message'], 'Response should contain error message')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_unauthorized_update(self):
         
        """
        This test ensures that user is unable to update food that was not created by him when making PUT call to the food/:id endpoint
        """
         
        user = User.objects.create_user('username', 'email', 'password')
        food = Food.objects.create(user=user, name='tomato')
         
        # hit the API endpoint
        response = self.client.put(reverse('food-detail', kwargs={'pk': food.id}), {"name": 'new_name', "description": ""})
         
        # check response
        self.assertIsNotNone(response.data['message'], 'Response should contain error message')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        