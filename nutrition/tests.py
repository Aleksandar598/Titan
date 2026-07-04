from django.contrib.auth.models import User
import datetime
from django.test import TestCase

from users.models import CustomUser
from .forms import FoodCreationForm
from .models import Food


# Create your tests here.

class FoodCreationFormTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username="user", email="example@email.com",
                                                   password="TheGreatPassword",
                                                   birth_date=datetime.date(1990, 1, 1),
                                                   height=120,
                                                   current_weight=100,
                                                   target_weight=120,
                                                   fitness_goal="gain")
        self.user2 = CustomUser.objects.create_user(username="user2", email="example2@email.com",
                                                   password="TheGreatPassword2",
                                                   birth_date=datetime.date(1990, 1, 1),
                                                   height=120,
                                                   current_weight=100,
                                                   target_weight=120,
                                                   fitness_goal="gain")
        self.existing_food = Food.objects.create(name="Apple",
                                                 calories=2,
                                                 proteins=2,
                                                 carbs=2,
                                                 fats=2,
                                                 created_by=self.user)
        self.form_data = {
            "name" : "pepper",
            "calories" : 100,
            "proteins" : 100,
            "carbs" : 100,
            "fats" : 100,
        }

    def test_form_valid(self):
        form = FoodCreationForm(data=self.form_data, user=self.user)
        self.assertTrue(form.is_valid())

    def test_form_0_calories(self):
        test_data = self.form_data.copy()
        test_data["calories"] = 0
        form = FoodCreationForm(data=test_data, user=self.user)
        self.assertFalse(form.is_valid())

    def test_form_negative_proteins(self):
        test_data = self.form_data.copy()
        test_data["proteins"] = -100
        form = FoodCreationForm(data=test_data, user=self.user)
        self.assertFalse(form.is_valid())

    def test_form_0_carbs(self):
        test_data = self.form_data.copy()
        test_data["carbs"] = -100
        form = FoodCreationForm(data=test_data, user=self.user)
        self.assertFalse(form.is_valid())

    def test_form_0_fats(self):
        test_data = self.form_data.copy()
        test_data["fats"] = -100
        form = FoodCreationForm(data=test_data, user=self.user)
        self.assertFalse(form.is_valid())

    def test_form_dublicate_food(self):
        test_data = self.form_data.copy()
        test_data["name"] = "Apple"
        form = FoodCreationForm(data=test_data, user=self.user)
        self.assertFalse(form.is_valid())

    def test_form_same_name_different_users(self):
        test_data = self.form_data.copy()
        test_data["name"] = "Apple"
        form = FoodCreationForm(data=test_data, user=self.user2)