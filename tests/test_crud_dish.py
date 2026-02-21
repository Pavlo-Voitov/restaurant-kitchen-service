from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from kitchen.models import DishType, Dish, Ingredient


class DishCrudTests(TestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="u1",
            password="pass12345"
        )

        self.client.login(username="u1", password="pass12345")

        self.type = DishType.objects.create(name="Soups")

        self.ingredient = Ingredient.objects.create(name="Salt")

        self.dish = Dish.objects.create(
            name="Tomato",
            description="Nice",
            price="10.00",
            dish_type=self.type
        )

        self.dish.cooks.add(self.user)

    # ---------------- CREATE ----------------

    def test_create_dish_with_formset(self):

        url = reverse("kitchen:dish-create")

        data = {

            # MAIN FORM
            "name": "Miso",
            "description": "Tasty soup",
            "price": "12.00",
            "dish_type": self.type.pk,

            # FORMSET MANAGEMENT
            "dishingredient_set-TOTAL_FORMS": "1",
            "dishingredient_set-INITIAL_FORMS": "0",
            "dishingredient_set-MIN_NUM_FORMS": "0",
            "dishingredient_set-MAX_NUM_FORMS": "1000",

            # FORMSET DATA
            "dishingredient_set-0-ingredient": self.ingredient.pk,
            "dishingredient_set-0-amount": "2",
            "dishingredient_set-0-unit": "g",
        }

        response = self.client.post(url, data, follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            Dish.objects.filter(name="Miso").exists()
        )

    # ---------------- UPDATE ----------------

    def test_update_dish_with_formset(self):

        url = reverse("kitchen:dish-update", kwargs={"pk": self.dish.pk})

        data = {

            "name": "Tomato Updated",
            "description": "Updated",
            "price": "15.00",
            "dish_type": self.type.pk,

            "dishingredient_set-TOTAL_FORMS": "1",
            "dishingredient_set-INITIAL_FORMS": "0",
            "dishingredient_set-MIN_NUM_FORMS": "0",
            "dishingredient_set-MAX_NUM_FORMS": "1000",

            "dishingredient_set-0-ingredient": self.ingredient.pk,
            "dishingredient_set-0-amount": "3",
            "dishingredient_set-0-unit": "g",
        }

        response = self.client.post(url, data, follow=True)

        self.assertEqual(response.status_code, 200)

        self.dish.refresh_from_db()

        self.assertEqual(self.dish.name, "Tomato Updated")
        self.assertEqual(str(self.dish.price), "15.00")

    # ---------------- DELETE ----------------

    def test_delete_dish(self):

        url = reverse("kitchen:dish-delete", kwargs={"pk": self.dish.pk})

        response = self.client.post(url, follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            Dish.objects.filter(pk=self.dish.pk).exists()
        )