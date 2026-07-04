from django.db import models
from django.conf import settings

from users.models import CustomUser


# Create your models here.

class Food(models.Model):
    name = models.CharField(max_length=200)
    fats = models.FloatField(verbose_name='Fats')
    proteins = models.FloatField(verbose_name='Proteins')
    carbs = models.FloatField(verbose_name='Carbs')
    calories = models.FloatField(verbose_name='Calories')

    REQUIRED_FIELDS = ['name', 'fats', 'proteins', 'carbs', 'calories']

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    api_food_id = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        unique=True,
    )

    def __str__(self):
        return f'{self.name} ({self.calories} kcal /100g)'

class MealLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    weight_grams = models.FloatField(verbose_name='Volume(grams)')
    logged_at = models.DateTimeField(auto_now_add=True, verbose_name='Logged at')

    def __str__(self):
        return f"{self.food} - {self.weight_grams} - {self.logged_at}"

    @property
    def total_calories(self):
        return (self.food.calories * self.weight_grams) / 100.0

    @property
    def total_proteins(self):
        return (self.food.proteins * self.weight_grams) / 100.0

    @property
    def total_carbs(self):
        return (self.food.carbs * self.weight_grams) / 100.0

    @property
    def total_fats(self):
        return (self.food.fats * self.weight_grams) / 100.0