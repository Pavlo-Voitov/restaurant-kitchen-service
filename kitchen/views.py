from django.shortcuts import render
from django.views import generic

from .models import Dish

class DishListView(generic.ListView):
    model = Dish
    paginate_by = 5
    context_object_name = "dishes"

class DishDetailView(generic.DetailView):
    model = Dish