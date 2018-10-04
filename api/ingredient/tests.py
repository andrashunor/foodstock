from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from django.contrib.auth.models import User
from api.food.models import Food
from .models import Ingredient
from .serializers import IngredientSerializer
from .services import IngredientService
from .dal import IngredientDAL

class AuthenticatedViewTest(APITestCase):
    client = APIClient()
        
    def setUp(self):
        
        # add test data
        user = User.objects.create_user('authuser', 'a@b.com', 'password')
        self.client.force_authenticate(user)

class IngredientCRUDTest(AuthenticatedViewTest):
    
    def test_create_ingredient(self):
        
        """
        This test ensures that ingredient can be created when we make POST call to the /ingredient endpoint
        """
        
        # hit the API endpoint
        response = self.client.post(reverse('ingredient-list'), {"name": "tomato", "description": ""})
        
        # check response
        ingredient = IngredientSerializer(data=response.data)
        self.assertIsNotNone(ingredient, 'Ingredient from data should exist')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                
    def test_successful_update_ingredient(self):
        
        """
        This test ensures that ingredient gets updated when we make PUT call to the ingredient/:id endpoint
        """
        new_name = 'new_name'
        ingredient = Ingredient.objects.create(name='old_name')
        
        # hit the API endpoint
        response = self.client.put(reverse('ingredient-detail', kwargs={'pk': ingredient.id}), {"name": 'new_name', "description": "new_description"})
        
        # check response
        self.assertEqual(new_name, response.data["name"], 'Name should been updated')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_partial_update_ingredient(self):
        
        """
        This test ensures that ingredient gets partially updated when we make PATCH call to the ingredient/:id endpoint
        """
        new_name = 'new_name'
        ingredient = Ingredient.objects.create(name='old_name')
        
        # hit the API endpoint
        response = self.client.patch(reverse('ingredient-detail', kwargs={'pk': ingredient.id}), {"name": 'new_name'})
        
        # check response
        self.assertEqual(new_name, response.data["name"], 'Name should been updated')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_ingredient(self):
        
        """
        This test ensures that ingredient gets deleted when we make DELETE call to the ingredient/:id endpoint
        """
        ingredient = Ingredient.objects.create(name='test')
        
        # hit the API endpoint
        response = self.client.delete(reverse('ingredient-detail', kwargs={'pk': ingredient.id}))
        
        # check response
        self.assertFalse(Ingredient.objects.filter(name='test').exists(), 'Ingredient should no longer exist in the database')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_get_ingredient(self):
        
        """
        This test ensures that ingredient can be fetched when we make GET call to the ingredient/:id endpoint
        """
        ingredient = Ingredient.objects.create(name='test')
        
        # hit the API endpoint
        response = self.client.get(reverse('ingredient-detail', kwargs={'pk': ingredient.id}))
        
        # check response
        test_against = IngredientSerializer(ingredient).data
        self.assertEqual(response.data, test_against, 'The ingredient data should be equal')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_create_ingredient_batch(self):
        
        """
        This test ensures that multiple ingredients can be created when we make POST call to the ingredients-create-batch/ endpoint
        """
        
        # hit the API endpoint
        response = self.client.post(reverse('ingredient-list'), [{"name": "tomato", "description": ""}, {"name": "tomato1", "description": ""}, {"name": "tomato2", "description": ""}, {"name": "tomato3", "description": ""}])
        
        expected = Ingredient.objects.all()
        serialized = IngredientSerializer(expected, many=True)
        
        # check response
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_ingredient_name_unique(self):
        
        """
        This test ensures that user is unable to create multiple ingredients with the same name when making POST call to the /ingredient endpoint
        """
        
        # hit the API endpoint
        Ingredient.objects.create(name='tomato', description="")
        response = self.client.post(reverse('ingredient-list'), {"name": "tomato", "description": ""})
        
        # check response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
