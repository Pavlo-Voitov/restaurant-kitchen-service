from django.urls import path

from .views import (index,
                    DishListView,
                    DishDetailView,
                    DishCreateView,
                    DishUpdateView,
                    DishDeleteView,
                    invite_me_to_create_dish,
                    DishTypeCreateView,
                    CookDetailView,
                    CookUpdateView,
                    DishTypeListView,
                    DishTypeUpdateView,
                    DishTypeDeleteView,
                    IngredientListView,
                    IngredientCreateView,
                    IngredientUpdateView,
                    IngredientDeleteView,)

urlpatterns = [
    path("", index, name="index"),
    path("dishes/",
         DishListView.as_view(),
         name="dish-list"),

    path("dishes/<int:pk>/",
         DishDetailView.as_view(),
         name="dish-detail"),

    path("dishes/create",
         DishCreateView.as_view(),
         name="dish-create"),

    path("dishes/<int:pk>/update/",
         DishUpdateView.as_view(),
         name="dish-update"),

    path("dishes/<int:pk>/delete/",
         DishDeleteView.as_view(),
         name="dish-delete"),

    path("dishes/<int:pk>/invite/",
         invite_me_to_create_dish,
         name="cook-invite"),

    path("dish_type/",
         DishTypeListView.as_view(),
         name="dish_type-list"),

    path("dish_type/create",
         DishTypeCreateView.as_view(),
         name="dish_type-create"),

    path("dish_type/<int:pk>/update",
         DishTypeUpdateView.as_view(),
         name="dish_type-update"),

    path("dish_type/<int:pk>/delete",
         DishTypeDeleteView.as_view(),
         name="dish_type-delete"),

    path("cook/<int:pk>/",
         CookDetailView.as_view(),
         name="cook-detail"),

    path("cook/me/update/",
         CookUpdateView.as_view(),
         name="cook-update"),

    path("ingredients/",
         IngredientListView.as_view(),
         name="ingredient-list"),

    path("ingredients/create",
         IngredientCreateView.as_view(),
         name="ingredient-create"),

    path("ingredients/<int:pk>/update",
         IngredientUpdateView.as_view(),
         name="ingredient-update"),

    path("ingredients/<int:pk>/delete",
         IngredientDeleteView.as_view(),
         name="ingredient-delete"),
]

app_name = "kitchen"
