from django import forms

from kitchen.models import Dish


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields ="__all__"