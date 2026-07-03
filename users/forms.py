from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import CustomUser, WeightHistory
from .validators import validate_maximum_weight, validate_minimum_weight, validate_birth_date, validate_fitness_goal, validate_realistic_height, MINIMUM_WEIGHT, MAXIMUM_WEIGHT

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
        validate_birth_date(birth_date)
        return birth_date

    def clean_height(self):
        height = self.cleaned_data.get('height')
        validate_realistic_height(height)
        return height

    def clean_current_weight(self):
        weight = self.cleaned_data.get('current_weight')
        validate_minimum_weight(weight)
        validate_maximum_weight(weight)
        return weight

    def clean_target_weight(self):
        target_weight = self.cleaned_data.get('target_weight')
        validate_minimum_weight(target_weight)
        validate_maximum_weight(target_weight)
        return target_weight

    def clean_fitness_goal(self):
        fitness_goal = self.cleaned_data.get('fitness_goal')
        cur_weight = self.cleaned_data.get('current_weight')
        target_weight = self.cleaned_data.get('target_weight')
        validate_fitness_goal(fitness_goal, cur_weight, target_weight)
        return fitness_goal

class LogWeightForm(forms.ModelForm):
    class Meta:
        model = WeightHistory
        fields = ['weight']
        widgets = {
            'weight' : forms.NumberInput(attrs={'step' : '0.1', 'min' : MINIMUM_WEIGHT, 'max' : MAXIMUM_WEIGHT}),
        }

    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        validate_minimum_weight(weight)
        validate_maximum_weight(weight)
        return weight


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['birth_date', 'height', 'target_weight', 'fitness_goal']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'height': forms.NumberInput(attrs={'step': '0.1'}),
            'target_weight': forms.NumberInput(attrs={'step': '0.1'}),
            'fitness_goal': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        validate_birth_date(birth_date)
        return birth_date

    def clean_height(self):
        height = self.cleaned_data.get('height')
        validate_realistic_height(height)
        return height

    def clean_target_weight(self):
        weight = self.cleaned_data.get('target_weight')
        validate_minimum_weight(weight)
        return weight

    def clean(self):
        cleaned_data = super().clean()
        fitness_goal = cleaned_data.get('fitness_goal')
        target_weight = cleaned_data.get('target_weight')
        current_weight = self.instance.current_weight
        if fitness_goal and target_weight is not None:
            try:
                validate_fitness_goal(fitness_goal, current_weight, target_weight)
            except ValidationError as e:
                self.add_error('fitness_goal', e)

        return cleaned_data