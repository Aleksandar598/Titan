from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    GOAL_CHOICES = [
        ('lose', 'Losing Weight'),
        ('maintain', 'Keep Weight'),
        ('gain', 'Gain Weight'),
    ]

    birth_date = models.DateField(verbose_name="Birth Date")
    height = models.FloatField(verbose_name="Height(cm)")
    current_weight = models.FloatField(verbose_name="Current Weight(kg)")
    target_weight = models.FloatField(verbose_name="Target Weight(kg)")
    fitness_goal = models.CharField(
        max_length=10,
        choices=GOAL_CHOICES,
        default='maintain',
        verbose_name="Fitness Goal",
    )

    def __str__(self):
        return self.username