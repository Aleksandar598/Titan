from django.db import models

from users.models import CustomUser


# Create your models here.


class Exercise(models.Model):
    EXERCISE_TYPES = ((3.5, "Machine"),
                      (4,'Calisthenics'),
                      (6,'Free weights'),
                      (8,'Crossfit')) #For a formula

    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    muscle_group = models.CharField(max_length = 100, blank=True, null=True)
    type_of_exercise = models.FloatField(max_length = 20, choices=EXERCISE_TYPES)

    def __str__(self):
        return self.name


class Workout(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    order = models.IntegerField()

    def __str__(self):
        return f"{self.workout} {self.exercise} {self.order}"

class ExerciseSet(models.Model):
    exercise = models.ForeignKey(WorkoutExercise, on_delete=models.CASCADE)
    weight = models.FloatField()
    count = models.IntegerField()
    set_number = models.IntegerField()

    def __str__(self):
        return f"{self.exercise} {self.weight} {self.count}"
