from django import forms
from django.contrib.auth import get_user_model

from kitchen.models import Dish, DishIngredient, DishType, Ingredient
from django.forms import inlineformset_factory


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ("name", "description", "price", "dish_type")


DishIngredientFormSet = inlineformset_factory(
    parent_model=Dish,
    model=DishIngredient,
    fields=("ingredient", "amount", "unit"),
    extra=1,
    can_delete=True,
)


class InviteCookForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label="Cook username",
    )


class DishTypeForm(forms.ModelForm):
    class Meta:
        model = DishType
        fields = "__all__"


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = "__all__"


class CookUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "years_of_experience", "email"]

    def clean_years_of_experience(self):
        years_of_experience = self.cleaned_data.get("years_of_experience")
        if years_of_experience is not None and years_of_experience < 0:
            raise forms.ValidationError("Experience cannot be negative.")
        return years_of_experience
