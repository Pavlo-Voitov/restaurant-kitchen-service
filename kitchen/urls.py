from django.urls import path

from .views import (DishListView,
                    DishDetailView, DishCreateView)

urlpatterns = [
    path("dishes/", DishListView.as_view(), name="dish-list"),
    path("dishes/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path("dishes/create", DishCreateView.as_view(), name="dish-create"),
]

app_name = "kitchen"