import requests
import os
import dotenv

dotenv.load_dotenv()
USDA_API_KEY = os.environ.get("USDA_API_KEY")

def get_api_result(query):
    if not query:
        return []

    URL = "https://api.nal.usda.gov/fdc/v1/foods/search"

    params = {
        'api_key': USDA_API_KEY,
        'query': query,
        'pageSize': 5,
        'dataType': ['Branded', 'Foundation']
    }

    try:
        response = requests.get(URL, params=params, timeout=5)
        response.raise_for_status()

        data = response.json()
        foods = data.get('foods', [])

        cleaned_results = []

        for food in foods:
            name = food.get('description', 'Неизвестен продукт')
            brand = food.get('brandOwner', '')
            full_name = f"{name} ({brand})" if brand else name

            nutrients = food.get('foodNutrients', [])

            calories = 0
            proteins = 0
            carbs = 0
            fats = 0

            for n in nutrients:
                n_id = n.get('nutrientId')
                value = n.get('value', 0)

                if n_id == 1008:
                    calories = value
                elif n_id == 1003:
                    proteins = value
                elif n_id == 1005:
                    carbs = value
                elif n_id == 1004:
                    fats = value

            api_id = food.get('fdcId', 'няма-ид')

            cleaned_results.append({
                'api_id': str(api_id),
                'name': full_name.title(),
                'calories': round(float(calories), 1),
                'proteins': round(float(proteins), 1),
                'carbs': round(float(carbs), 1),
                'fats': round(float(fats), 1),
            })

        return cleaned_results

    except Exception as e:
        print(f"❌ Грешка при връзка с USDA API: {e}")
        return []


# =====================================================================
#(Generated With AI)
# =====================================================================
if __name__ == "__main__":
    print("--- 🍏 Стартиране на тест с USDA API ---")

    # Тъй като базата данни е американска, търсенето работи отлично на английски
    test_word = "banana"
    print(f"📡 Търсене на: '{test_word}'...")

    results = get_api_result(test_word)

    print("\n--- 📊 Намерени резултати ---")
    if not results:
        print("Няма намерени резултати или възникна грешка с API ключа.")
    else:
        for item in results:
            print(f"Храна: {item['name']} (ID: {item['api_id']})")
            print(
                f"  За 100g -> Калории: {item['calories']} kcal | П: {item['proteins']}g | В: {item['carbs']}g | М: {item['fats']}g\n")