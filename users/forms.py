from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class TitanUserCreationForm(UserCreationForm):
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Birth Date"
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('birth_date', 'height', 'current_weight', 'target_weight', 'fitness_goal')