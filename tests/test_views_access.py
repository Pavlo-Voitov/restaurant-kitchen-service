from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from kitchen.models import DishType, Dish, Ingredient


class ViewAccessTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="u1", password="pass12345")

        self.dish_type = DishType.objects.create(name="Soups")
        self.ingredient = Ingredient.objects.create(name="Salt")
        self.dish = Dish.objects.create(
            name="Tomato Soup",
            description="Nice",
            price="10.00",
            dish_type=self.dish_type,
        )
        self.dish.cooks.add(self.user)

    def test_anonymous_redirected_from_pages(self):
        urls = [
            reverse("kitchen:dish-list"),
            reverse("kitchen:dish-detail", kwargs={"pk": self.dish.pk}),
            reverse("kitchen:dish-create"),
            reverse("kitchen:dish-update", kwargs={"pk": self.dish.pk}),
            reverse("kitchen:dish-delete", kwargs={"pk": self.dish.pk}),
            reverse("kitchen:dish_type-list"),
            reverse("kitchen:dish_type-create"),
            reverse("kitchen:ingredient-list"),
            reverse("kitchen:ingredient-create"),
        ]

        for url in urls:
            resp = self.client.get(url)
            self.assertIn(resp.status_code, (302, 301))
            self.assertIn("/accounts/login/", resp.url)

    def test_logged_in_can_open_pages(self):
        self.client.login(username="u1", password="pass12345")

        urls = [
            reverse("kitchen:dish-list"),
            reverse("kitchen:dish-detail", kwargs={"pk": self.dish.pk}),
            reverse("kitchen:dish-create"),
            reverse("kitchen:dish-update", kwargs={"pk": self.dish.pk}),
            reverse("kitchen:dish-delete", kwargs={"pk": self.dish.pk}),
            reverse("kitchen:dish_type-list"),
            reverse("kitchen:dish_type-create"),
            reverse("kitchen:ingredient-list"),
            reverse("kitchen:ingredient-create"),
        ]

        for url in urls:
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 200)