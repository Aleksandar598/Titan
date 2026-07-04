from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import FoodCreationForm
from .models import Food, MealLog
from .FoodApi import get_api_result

# Create your views here.

@login_required
def nutrition_view(request):
    return render(request, 'nutrition/nutrition.html')

@login_required
def create_food_view(request):
    if request.method == 'POST':
        form = FoodCreationForm(request.POST, user=request.user)
        if form.is_valid():
            food = form.save(commit=False)
            food.created_by = request.user
            food.save()
            return redirect('dashboard')
    else:
        form = FoodCreationForm(user=request.user)
    return render(request, 'nutrition/create_food.html', {'form': form})

@login_required
def log_food_view(request):
    results = []
    db_result = []
    query = request.GET.get('query', '')
    if query:
        db_result = Food.objects.filter(created_by=request.user, name__icontains=query)
        results = get_api_result(query)

    if request.method == 'POST':
        api_id = request.POST.get('api_id')
        food_name = request.POST.get('food_name')
        calories = float(request.POST.get('calories', 0))
        proteins = float(request.POST.get('proteins', 0))
        carbs = float(request.POST.get('carbs', 0))
        fats = float(request.POST.get('fats', 0))

        weight_grams = float(request.POST.get('weight_grams', 100))
        food_obj, created = Food.objects.get_or_create(
            api_food_id=api_id,
            defaults={
                'name': food_name,
                'calories': calories,
                'proteins': proteins,
                'carbs': carbs,
                'fats': fats
            }
        )
        MealLog.objects.create(
            user=request.user,
            food=food_obj,
            weight_grams=weight_grams
        )
        return redirect('nutrition')

    context = {
        'db_result': db_result,
        'results': results,
        'query': query
    }
    return render(request, 'nutrition/log_food.html', context)