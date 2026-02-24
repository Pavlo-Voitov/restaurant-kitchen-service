from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from kitchen.models import DishType, Ingredient, Dish, DishIngredient


class ModelTests(TestCase):
    def test_dish_type_str(self):
        dish_type = DishType.objects.create(name="Soups")
        self.assertEqual(str(dish_type), "Soups")

    def test_ingredient_str(self):
        ingredient = Ingredient.objects.create(name="Salt")
        self.assertEqual(str(ingredient), "Salt")

    def test_cook_str(self):
        Cook = get_user_model()
        cook = Cook.objects.create_user(
            username="cook_pasha", password="12345",
            first_name="Pasha", last_name="Voitov"
        )
        self.assertIn("cook_pasha", str(cook))

    def test_dishingredient_unique_constraint(self):
        Cook = get_user_model()
        cook = Cook.objects.create_user(username="c1", password="12345")
        dish_type = DishType.objects.create(name="Soups")
        dish = Dish.objects.create(name="Tomato", price=10, dish_type=dish_type)
        dish.cooks.add(cook)

        ingredient = Ingredient.objects.create(name="Salt")

        DishIngredient.objects.create(dish=dish,
                                      ingredient=ingredient,
                                      amount=1, unit="g")

        with self.assertRaises(IntegrityError):
            DishIngredient.objects.create(dish=dish,
                                          ingredient=ingredient,
                                          amount=2,
                                          unit="g")

    def test_cook_get_absolute_url(self):
        Cook = get_user_model()
        cook = Cook.objects.create_user(username="cook_pasha", password="12345")
        self.assertIn(f"/cook/{cook.pk}/", cook.get_absolute_url())

    def test_dish_get_absolute_url(self):
        dish_type = DishType.objects.create(name="Soups")
        dish = Dish.objects.create(
            name="Tomato Soup",
            description="Nice",
            price="91.00",
            dish_type=dish_type
        )
        self.assertIn(f"/dishes/{dish.pk}/", dish.get_absolute_url())
