from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic.list import MultipleObjectMixin

from .forms import DishForm, DishIngredientFormSet, InviteCookForm, CookUpdateForm, DishTypeForm, IngredientForm
from .models import Dish, DishType, Cook, Ingredient


@login_required
def index(request):
    return redirect("kitchen:dish-list")


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    paginate_by = 5
    context_object_name = "dishes"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishListView, self).get_context_data(**kwargs)

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

class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    paginate_by = 5
    context_object_name = "types"
    template_name = "kitchen/dish_type_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishTypeListView, self).get_context_data(**kwargs)

        search_query = self.request.GET.get("search")
        context["search_query"] = search_query

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(name__icontains=search)

        return queryset


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model =DishType
    form_class = DishTypeForm
    template_name = "kitchen/dish_type_form.html"
    success_url = reverse_lazy("kitchen:dish_type-list")

    def form_valid(self, form):
        messages.success(self.request, "Dish type update successfully!")
        return super().form_valid(form)


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    success_url = reverse_lazy("kitchen:dish_type-list")

    def form_valid(self, form):
        messages.success(self.request, "Dish type deleted successfully!")
        return super().form_valid(form)


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish


class CookDetailView(LoginRequiredMixin, generic.DetailView, MultipleObjectMixin):
    model = get_user_model()
    template_name = "kitchen/cook_detail.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        dishes = self.object.dishes.select_related("dish_type")

        search = self.request.GET.get("search")
        if search:
            dishes = dishes.filter(name__icontains=search)

        context = super().get_context_data(object_list=dishes, **kwargs)
        context["search_query"] = search

        return context


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dish-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.method == "POST":
            context["formset"] = DishIngredientFormSet(self.request.POST)
        else:
            context["formset"] = DishIngredientFormSet()

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]

        if not formset.is_valid():
            return self.form_invalid(form)

        self.object = form.save()
        self.object.cooks.add(self.request.user)
        formset.instance = self.object
        formset.save()
        messages.success(self.request, "Dish created successfully!")

        return super().form_valid(form)


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    form_class = DishTypeForm
    template_name = "kitchen/dish_type_form.html"
    success_url = reverse_lazy("kitchen:dish-list")

    def form_valid(self, form):
        messages.success(self.request, "Type of dish created successfully!")
        return super().form_valid(form)


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


class IngredientListView(LoginRequiredMixin, generic.ListView):
    model = Ingredient
    paginate_by = 5
    context_object_name = "ingredients"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IngredientListView, self).get_context_data(**kwargs)

        search_query = self.request.GET.get("search")
        context["search_query"] = search_query

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(name__icontains=search)

        return queryset



class IngredientCreateView(LoginRequiredMixin, generic.CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = "kitchen/ingredient_form.html"
    success_url = reverse_lazy("kitchen:ingredient-list")

    def form_valid(self, form):
        messages.success(self.request, "Ingredient created successfully!")
        return super().form_valid(form)


class IngredientUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = "kitchen/ingredient_form.html"
    success_url = reverse_lazy("kitchen:ingredient-list")

    def form_valid(self, form):
        messages.success(self.request, "Ingredient updated successfully!")
        return super().form_valid(form)


class IngredientDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Ingredient
    success_url = reverse_lazy("kitchen:ingredient-list")

    def form_valid(self, form):
        messages.success(self.request, "Ingredient deleted successfully!")
        return super().form_valid(form)


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