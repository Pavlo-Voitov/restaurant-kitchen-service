from django import forms

from kitchen.models import Dish, DishIngredient
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