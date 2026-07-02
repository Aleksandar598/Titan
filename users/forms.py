from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import CustomUser

class TitanUserCreationForm(UserCreationForm):
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Birth Date"
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'birth_date', 'height', 'current_weight', 'target_weight', 'fitness_goal')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("A user with this email address already exists.")
        return email

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date and birth_date > timezone.now().date():
            raise ValidationError("Birth Date cannot be in the future")
        return birth_date

    def clean_height(self):
        height = self.cleaned_data.get('height')
        if height < 80:
            raise ValidationError("Height cannot be less than 80")
        return height

    def clean_current_weight(self):
        weight = self.cleaned_data.get('current_weight')
        if weight < 20 or weight > 500:
            raise ValidationError("Weight must be realistic")
        return weight

    def clean_target_weight(self):
        target_weight = self.cleaned_data.get('target_weight')
        if target_weight < 20 or target_weight > 300:
            raise ValidationError("Target weight must be realistic.")
        return target_weight

    def clean_fitness_goal(self):
        fitness_goal = self.cleaned_data.get('fitness_goal')
        cur_weight = self.cleaned_data.get('current_weight')
        target_weight = self.cleaned_data.get('target_weight')
        if cur_weight is None or target_weight is None:
            return fitness_goal

        if fitness_goal == "maintain":
            if cur_weight != target_weight:
                raise ValidationError("Fitness goal must be equal to target weight")
        if fitness_goal == "gain":
            if cur_weight >= target_weight:
                raise ValidationError("Fitness goal must be less than target weight")
        if fitness_goal == "lose":
            if cur_weight <= target_weight:
                raise ValidationError("Fitness goal must be less than target weight")
        return fitness_goal