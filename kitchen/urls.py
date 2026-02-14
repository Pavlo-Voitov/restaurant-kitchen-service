from django.urls import path

from .views import (index,
                    DishListView,
                    DishDetailView,
                    DishCreateView,
                    DishUpdateView,
                    DishDeleteView,
                    invite_me_to_create_dish,
                    DishTypeCreateView, CookDetailView, CookUpdateView, )

urlpatterns = [
    path("", index, name="index"),
    path("dishes/", DishListView.as_view(), name="dish-list"),
    path("dishes/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path("dishes/create", DishCreateView.as_view(), name="dish-create"),
    path("dishes/<int:pk>/update/", DishUpdateView.as_view(), name="dish-update"),
    path("dishes/<int:pk>/delete/", DishDeleteView.as_view(), name="dish-delete"),
    path("dishes/<int:pk>/invite/", invite_me_to_create_dish, name="cook-invite"),
    path("dish_type/create", DishTypeCreateView.as_view(), name="dish_type-create"),
    path("cook/<int:pk>/", CookDetailView.as_view(), name="cook-detail"),
    path("cook/me/update/", CookUpdateView.as_view(), name="cook-update"),
]

app_name = "kitchen"