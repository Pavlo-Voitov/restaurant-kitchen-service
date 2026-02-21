from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from kitchen.models import DishType


class DishTypeCrudTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="u1", password="pass12345")
        self.client.login(username="u1", password="pass12345")
        self.type1 = DishType.objects.create(name="Soups")

    def test_create_dish_type(self):
        url = reverse("kitchen:dish_type-create")
        resp = self.client.post(url, data={"name": "Pasta"}, follow=True)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(DishType.objects.filter(name="Pasta").exists())

    def test_update_dish_type(self):
        url = reverse("kitchen:dish_type-update", kwargs={"pk": self.type1.pk})
        resp = self.client.post(url, data={"name": "Soups Updated"}, follow=True)

        self.assertEqual(resp.status_code, 200)
        self.type1.refresh_from_db()
        self.assertEqual(self.type1.name, "Soups Updated")

    def test_delete_dish_type(self):
        url = reverse("kitchen:dish_type-delete", kwargs={"pk": self.type1.pk})
        resp = self.client.post(url, follow=True)

        self.assertEqual(resp.status_code, 200)
        self.assertFalse(DishType.objects.filter(pk=self.type1.pk).exists())