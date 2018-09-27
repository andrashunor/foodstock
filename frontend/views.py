from django.views import generic
from api.models import Food
from api.services import FoodService
from django.contrib.auth.models import User


# Create your views here.

class IndexView(generic.ListView):
    template_name = 'frontend/index.html'
    context_object_name = 'food_list'
    
    def get_queryset(self):
        """
        List of food object for user
        """
        
        user = User.objects.get(pk=1)
        service = FoodService()
        return service.get_foods(user=user)


class DetailView(generic.DetailView):
    model = Food
    template_name = 'frontend/detail.html'
    
    def get_object(self, queryset=None):
        """
        Detail of specific food object for user
        """
        
        user = User.objects.get(pk=1)
        if 'pk' in self.kwargs:
            service = FoodService()
            return service.get_object(pk=self.kwargs['pk'], user=user)
        return None

