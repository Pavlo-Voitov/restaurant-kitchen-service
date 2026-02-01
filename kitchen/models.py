from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Cook(AbstractUser):
    years_of_experience = models.IntegerField(null=True, blank=True)
