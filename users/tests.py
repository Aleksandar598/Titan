from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
import datetime
from users.models import CustomUser, WeightHistory
from users.forms import TitanUserCreationForm, LogWeightForm, UpdateUserForm


class TitanUserCreationFormTest(TestCase):

    def setUp(self):
        self.existing_user = CustomUser.objects.create_user(
            username="existing_user",
            email="taken@example.com",
            password="password123",
            birth_date=datetime.date(1990, 1, 1),
            height=100,
            current_weight=100,
            target_weight=100,
            fitness_goal="maintain"
        )

        self.valid_data = {
            'username': 'new_user',
            'email': 'new@example.com',
            'birth_date': '1995-05-15',
            'height': 175.5,
            'current_weight': 70.0,
            'target_weight': 68.0,
            'fitness_goal': 'lose',
            'password1': 'secretpass123',
            'password2': 'secretpass123',
        }

    def test_form_valid(self):
        form = TitanUserCreationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_dublicate_email(self):
        data = self.valid_data.copy()
        data['email'] = self.existing_user.email
        form = TitanUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_future_birth_date(self):
        data = self.valid_data.copy()
        future_date = (timezone.now() + datetime.timedelta(days=1)).date()
        data['birth_date'] = future_date.strftime('%Y-%m-%d')
        form = TitanUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('birth_date', form.errors)

    def test_unrealistic_height(self):
        data = self.valid_data.copy()
        data['height'] = 2
        form = TitanUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('height', form.errors)

    def test_unrealistic_current_weight(self):
        data = self.valid_data.copy()
        data['current_weight'] = 1
        form = TitanUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('current_weight', form.errors)

    def test_unrealistic_target_weight(self):
        data = self.valid_data.copy()
        data['current_weight'] = 100
        data['target_weight'] = 2
        data['fitness_goal'] = 'lose'
        form = TitanUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('target_weight', form.errors)

    def test_unrealistic_fitness_goal_gain_weight(self):
        data = self.valid_data.copy()
        data['fitness_goal'] = 'gain'
        data['current_weight'] = 100
        data['target_weight'] = 100
        form = TitanUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('fitness_goal', form.errors)

    def test_unrealistic_fitness_goal_lose_weight(self):
        data = self.valid_data.copy()
        data['fitness_goal'] = 'lose'
        data['current_weight'] = 100
        data['target_weight'] = 100
        form = TitanUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('fitness_goal', form.errors)

    def test_unrealistic_fitness_goal_keep_weight(self):
        data = self.valid_data.copy()
        data['fitness_goal'] = 'lose'
        data['current_weight'] = 100
        data['target_weight'] = 120
        form = TitanUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('fitness_goal', form.errors)

class WeightHistoryTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="user", email="example@email.com",
                                                   password="TheGreatPassword",
                                                   birth_date=datetime.date(1990, 1, 1),
                                                   height=120,
                                                   current_weight=100,
                                                   target_weight=120,
                                                   fitness_goal="gain")
        self.url = reverse('log_weight')

    def test_form_valid(self):
        form = LogWeightForm(data={'weight' : 50.2})
        self.assertTrue(form.is_valid())

    def test_form_low_weight(self):
        form = LogWeightForm(data={'weight' : 10})
        self.assertFalse(form.is_valid())

    def test_form_high_weight(self):
        form = LogWeightForm(data={'weight' : 12000})
        self.assertFalse(form.is_valid())

    def test_view_logout_view(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_successful_weight_log(self):
        self.client.login(username=self.user.username, password="TheGreatPassword")
        response = self.client.post(self.url, data={'weight' : 100.2} )
        print("REDIRECT URL TO:", response.get('Location'))
        self.assertEqual(response.status_code, 302)

        self.assertEqual(WeightHistory.objects.filter(user=self.user).count(), 1)
        latest_log = WeightHistory.objects.filter(user=self.user).first()
        self.assertEqual(latest_log.weight, 100.2)

        self.user.refresh_from_db()
        self.assertEqual(self.user.current_weight, 100.2)

class UserUpdateTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="user", email="example@email.com",
                                                   password="TheGreatPassword",
                                                   birth_date=datetime.date(1990, 1, 1),
                                                   height=120,
                                                   current_weight=100,
                                                   target_weight=120,
                                                   fitness_goal="gain")
        self.url = reverse('update_user_info')
    def test_form_valid(self):
        form_data = {
            'birth_date': '1993-02-02',
            'height': '180',
            'target_weight': '200',
            'fitness_goal': 'gain'
        }
        form = UpdateUserForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_form_invalid_fitness_goal(self):
        form_data = {
            'birth_date': '1993-02-02',
            'height': '180',
            'target_weight': '200',
            'fitness_goal': 'lose'
        }
        form = UpdateUserForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())

    def test_form_invalid_height(self):
        form_data = {
            'birth_date': '1993-02-02',
            'height': '2',
            'target_weight': '200',
            'fitness_goal': 'lose'
        }
        form = UpdateUserForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())

    def test_view_logout_redirect(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_database_update_on_success(self):
        self.client.login(username="user", password="TheGreatPassword")
        form_data = {
            'birth_date': '1990-01-01',
            'height': '150',
            'target_weight': '80',
            'fitness_goal': 'lose'
        }
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.target_weight, 80)
        self.assertEqual(self.user.fitness_goal, 'lose')
        self.assertEqual(self.user.birth_date, datetime.date(1990, 1, 1))
        self.assertEqual(self.user.height, 150)