from django.urls import path

from .views import DishListView

urlpatterns = [
    path("dishes/", DishListView.as_view(), name="dish-list"),
    path("dishes/<int:pk>/", DishListView.as_view(), name="dish-detail")
]

app_name = "kitchen"