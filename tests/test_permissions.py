from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from kitchen.models import DishType, Dish


class DishPermissionTests(TestCase):
    def setUp(self):
        Cook = get_user_model()
        self.owner = Cook.objects.create_user(username="owner", password="12345")
        self.other = Cook.objects.create_user(username="other", password="12345")

        self.dish_type = DishType.objects.create(name="Soups")
        self.dish = Dish.objects.create(
            name="Tomato Soup",
            description="Nice",
            price="91.00",
            dish_type=self.dish_type
        )
        self.dish.cooks.add(self.owner)

    def test_anonymous_redirected_from_dish_list(self):
        url = reverse("kitchen:dish-list")
        res = self.client.get(url)
        self.assertNotEqual(res.status_code, 200)
        self.assertIn("/accounts/login/", res.url)

    def test_logged_in_can_open_dish_detail(self):
        self.client.login(username="owner", password="12345")
        url = reverse("kitchen:dish-detail", kwargs={"pk": self.dish.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_non_cook_cannot_open_update(self):
        self.client.login(username="other", password="12345")
        url = reverse("kitchen:dish-update", kwargs={"pk": self.dish.pk})
        res = self.client.get(url)
        self.assertIn(res.status_code, (403, 302))

    def test_owner_can_open_update(self):
        self.client.login(username="owner", password="12345")
        url = reverse("kitchen:dish-update", kwargs={"pk": self.dish.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)