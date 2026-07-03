from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import TitanUserCreationForm, LogWeightForm
from .models import WeightHistory


def register_view(request):
    if request.method == 'POST':
        form = TitanUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = TitanUserCreationForm()

    return render(request, 'users/register.html', {'form': form})

@login_required
def log_weight_view(request):
    if request.method == 'POST':
        form = LogWeightForm(request.POST)
        if form.is_valid():
            weight = form.save(commit=False)
            weight.user = request.user
            weight.save()

            request.user.current_weight = weight.weight
            request.user.save(update_fields=['current_weight'])

            return redirect('log_weight')
    else:
        form = LogWeightForm()

    logs = WeightHistory.objects.filter(user=request.user)
    return render(request, 'users/log_weight.html', {'form': form, 'logs': logs})
