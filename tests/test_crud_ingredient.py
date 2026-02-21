from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from kitchen.models import Ingredient


class IngredientCrudTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="u1", password="pass12345")
        self.client.login(username="u1", password="pass12345")
        self.ing = Ingredient.objects.create(name="Salt")

    def test_create_ingredient(self):
        url = reverse("kitchen:ingredient-create")
        resp = self.client.post(url, data={"name": "Pepper"}, follow=True)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(Ingredient.objects.filter(name="Pepper").exists())

    def test_update_ingredient(self):
        url = reverse("kitchen:ingredient-update", kwargs={"pk": self.ing.pk})
        resp = self.client.post(url, data={"name": "Salt Updated"}, follow=True)

        self.assertEqual(resp.status_code, 200)
        self.ing.refresh_from_db()
        self.assertEqual(self.ing.name, "Salt Updated")

    def test_delete_ingredient(self):
        url = reverse("kitchen:ingredient-delete", kwargs={"pk": self.ing.pk})
        resp = self.client.post(url, follow=True)

        self.assertEqual(resp.status_code, 200)
        self.assertFalse(Ingredient.objects.filter(pk=self.ing.pk).exists())