from django.db.models import Count
from django.shortcuts import render
from django.views import generic

from .models import Dish, DishType, Cook


class DishListView(generic.ListView):
    model = Dish
    paginate_by = 5
    context_object_name = "dishes"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishListView, self).get_context_data(**kwargs)

        types_of_dish = DishType.objects.annotate(dishes_count=Count("dishes"))
        context["types_of_dish"] = types_of_dish

        selected_dish_type = self.request.GET.get("dish_type")
        context["selected_dish_type"] = int(selected_dish_type) if selected_dish_type else None

        cooks = Cook.objects.all()
        selected_cook = self.request.GET.get("cook")
        context["cooks"] = cooks
        context["selected_cook"] = int(selected_cook) if selected_cook else None

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related("dish_type").annotate(cooks_count=Count("cooks", distinct=True))

        dish_type = self.request.GET.get("dish_type")
        if dish_type:
            queryset = queryset.filter(dish_type_id=int(dish_type))

        cook = self.request.GET.get("cook")
        if cook:
            queryset = queryset.filter(cooks__id=int(cook)).distinct()

        return queryset


class DishDetailView(generic.DetailView):
    model = Dish