from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from kitchen.models import DishType, Dish


class DishListFiltersTests(TestCase):
    def setUp(self):
        Cook = get_user_model()
        self.c1 = Cook.objects.create_user(username="c1", password="12345")
        self.c2 = Cook.objects.create_user(username="c2", password="12345")

        self.t_soup = DishType.objects.create(name="Soups")
        self.t_pasta = DishType.objects.create(name="Pasta")

        self.d1 = Dish.objects.create(name="Tomato Soup",
                                      description="a",
                                      price="10.00",
                                      dish_type=self.t_soup)
        self.d2 = Dish.objects.create(name="Miso Soup",
                                      description="b",
                                      price="11.00",
                                      dish_type=self.t_soup)
        self.d3 = Dish.objects.create(name="Carbonara",
                                      description="c",
                                      price="12.00",
                                      dish_type=self.t_pasta)

        self.d1.cooks.add(self.c1)
        self.d2.cooks.add(self.c2)
        self.d3.cooks.add(self.c1)

        self.client.login(username="c1", password="12345")

    def test_filter_by_dish_type(self):
        url = reverse("kitchen:dish-list")
        res = self.client.get(url, {"dish_type": self.t_pasta.id})
        self.assertContains(res, "Carbonara")
        self.assertNotContains(res, "Tomato Soup")

    def test_filter_by_cook(self):
        url = reverse("kitchen:dish-list")
        res = self.client.get(url, {"cook": self.c2.id})
        self.assertContains(res, "Miso Soup")
        self.assertNotContains(res, "Carbonara")

    def test_filter_by_search(self):
        url = reverse("kitchen:dish-list")
        res = self.client.get(url, {"search": "miso"})
        self.assertContains(res, "Miso Soup")
        self.assertNotContains(res, "Tomato Soup")

    def test_filter_combined(self):
        url = reverse("kitchen:dish-list")
        res = self.client.get(url, {"dish_type": self.t_soup.id, "cook": self.c2.id})
        self.assertContains(res, "Miso Soup")
        self.assertNotContains(res, "Tomato Soup")
