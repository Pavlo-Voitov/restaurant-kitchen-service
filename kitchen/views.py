from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import DishForm
from .models import Dish, DishType, Cook


@login_required
def index(request):
    return redirect("kitchen:dish-list")


class DishListView(LoginRequiredMixin, generic.ListView):
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

        search_query = self.request.GET.get("search")
        context["search_query"] = search_query

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

        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(name__icontains=search)

        return queryset


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dish-list")

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.cooks.add(self.request.user)
        messages.success(self.request, "Dish created successfully!")
        return response


class DishUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Dish
    form_class = DishForm

    def test_func(self):
        dish = self.get_object()
        return self.request.user in dish.cooks.all()

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Dish updated successfully!")
        return response


class DishDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("kitchen:dish-list")

    def test_func(self):
        dish = self.get_object()
        return self.request.user in dish.cooks.all()

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Dish deleted successfully!")
        return response