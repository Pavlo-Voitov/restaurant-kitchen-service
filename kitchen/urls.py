from django.urls import path

from .views import (index,
                    DishListView,
                    DishDetailView,
                    DishCreateView,
                    DishUpdateView,
                    DishDeleteView,
                    invite_me_to_create_dish,)

urlpatterns = [
    path("", index, name="index"),
    path("dishes/", DishListView.as_view(), name="dish-list"),
    path("dishes/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path("dishes/create", DishCreateView.as_view(), name="dish-create"),
    path("dishes/<int:pk>/update/", DishUpdateView.as_view(), name="dish-update"),
    path("dishes/<int:pk>/delete/", DishDeleteView.as_view(), name="dish-delete"),
    path("dishes/<int:pk>/invite/", invite_me_to_create_dish, name="cook-invite"),
]

app_name = "kitchen"