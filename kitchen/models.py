from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


# Create your models here.
class Cook(AbstractUser):
    years_of_experience = models.IntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    class Meta:
        verbose_name = "cook"
        verbose_name_plural = "cooks"

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("kitchen:cook-detail", kwargs={"pk": self.pk})


class DishType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    dish_type = models.ForeignKey(DishType, on_delete=models.CASCADE, related_name="dishes")
    cooks = models.ManyToManyField(Cook, related_name="dishes")
    ingredients = models.ManyToManyField("Ingredient",
                                         related_name="dishes",
                                         blank=True,
                                         through="DishIngredient",)

    def __str__(self):
        return f"{self.name} with price: {self.price}"

    def get_absolute_url(self):
        return reverse("kitchen:dish-detail", kwargs={"pk": self.pk})


class Ingredient(models. Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class DishIngredient(models.Model):
    class Unit(models.TextChoices):
        G = "g", "g"
        ML = "ml", "ml"
        PCS = "pcs", "pcs"
        TSP = "tsp", "tsp"
        TBSP = "tbsp", "tbsp"

    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    unit = models.CharField(max_length=10, choices=Unit.choices, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["dish", "ingredient"], name="unique_dish_ingredient")
        ]

    def __str__(self):
        return f"{self.dish} - {self.ingredient}"
