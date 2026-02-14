from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic.list import MultipleObjectMixin

from .forms import DishForm, DishIngredientFormSet, InviteCookForm, DishTypeCreateForm, CookUpdateForm
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


class CookDetailView(LoginRequiredMixin, generic.DetailView, MultipleObjectMixin):
    model = get_user_model()
    template_name = "kitchen/cook_detail.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        dishes = self.object.dishes.all().select_related("dish_type")
        context = super().get_context_data(object_list=dishes, **kwargs)
        return context


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dish-list")

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.cooks.add(self.request.user)
        messages.success(self.request, "Dish created successfully!")
        return response


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    form_class = DishTypeCreateForm
    template_name = "kitchen/dish_type_form.html"
    success_url = reverse_lazy("kitchen:dish-list")


class DishUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Dish
    form_class = DishForm
    template_name = "kitchen/dish_form.html"
    success_url = reverse_lazy("kitchen:dish-list")

    def test_func(self):
        dish = self.get_object()
        return self.request.user in dish.cooks.all()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = DishIngredientFormSet(instance=self.object)
        return render(request, self.template_name, {"form": form,
                                                    "formset": formset,
                                                    "object": self.object,})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = DishIngredientFormSet(request.POST, instance=self.object)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Dish updated successfully!")
            return redirect(self.success_url)

        return render(request, self.template_name, {"form": form,
                                                    "formset": formset,
                                                    "object": self.object,})

class CookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = CookUpdateForm
    template_name = "kitchen/cook_update_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Cook updated successfully!")
        return response

    def get_success_url(self):
        return reverse_lazy("kitchen:cook-detail", kwargs={"pk": self.object.pk})

    def get_object(self, queryset=None):
        return self.request.user


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



@login_required
def invite_me_to_create_dish(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    form = InviteCookForm(request.POST)

    if form.is_valid():
        username = form.cleaned_data["username"]
    else:
        messages.error(request, "Invalid form.")
        return redirect("kitchen:dish-detail", pk=pk)

    try:
        cook = Cook.objects.get(username=username)
    except:
        messages.error(request, "User not found.")
        return redirect("kitchen:dish-detail", pk=pk)

    dish.cooks.add(cook)
    messages.success(request, f"{username} was added as cook.")
    return redirect("kitchen:dish-detail", pk=pk)