from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import TitanUserCreationForm, LogWeightForm, UpdateUserForm
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

@login_required
def dashboard_view(request):
    return render(request, 'users/dashboard.html')

@login_required
def update_user_info(request):
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('update_user_info')
    else:
        form = UpdateUserForm(instance=request.user)
    return render(request, 'users/update_user_info.html', {'form': form})

