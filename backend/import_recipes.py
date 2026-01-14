import requests
import json
import os
import string
import time

# TheMealDB Free API Endpoints
# We use search by first letter to get bulk data efficiently
BASE_URL = "https://www.themealdb.com/api/json/v1/1/search.php?f="

def format_recipe(meal_data, new_id):
    # Extract ingredients
    ingredients = []
    for i in range(1, 21):
        ing = meal_data.get(f'strIngredient{i}')
        if ing and ing.strip():
            ingredients.append(ing.strip())

    # Generate Hints
    hints = []
    
    # Hint 1: Origin
    if meal_data.get('strArea'):
        hints.append(f"Origin: {meal_data['strArea']}")
    
    # Hint 2: Category
    if meal_data.get('strCategory'):
        hints.append(f"Category: {meal_data['strCategory']}")
    
    # Hint 3: Key Ingredient (Random one to make it harder)
    if len(ingredients) > 0:
        # Pick a middle ingredient to avoid giving away the main protein immediately if possible
        idx = len(ingredients) // 2
        hints.append(f"Contains {ingredients[idx]}")
    
    # Hint 4: First Letter
    hints.append(f"Starts with '{meal_data['strMeal'][0]}'")

    return {
        "id": new_id,
        "name": meal_data['strMeal'],
        "image": meal_data['strMealThumb'],
        "ingredients": ingredients,
        "hints": hints
    }

def generate_bulk_dataset(target_count=500):
    print(f"Starting bulk import for ~{target_count} unique recipes...")
    
    new_recipes = []
    seen_names = set()
    current_id = 1
    
    # Iterate A-Z to get a wide variety of "trending" standard recipes
    # This is much faster and cleaner than hitting random endpoint 
    for letter in string.ascii_lowercase:
        if len(new_recipes) >= target_count:
            break
            
        print(f"Fetching recipes starting with '{letter}'...")
        try:
            res = requests.get(f"{BASE_URL}{letter}")
            data = res.json()
            
            if data and data['meals']:
                for meal in data['meals']:
                    if len(new_recipes) >= target_count:
                        break
                        
                    if meal['strMeal'] not in seen_names:
                        formatted = format_recipe(meal, current_id)
                        new_recipes.append(formatted)
                        seen_names.add(meal['strMeal'])
                        current_id += 1
        except Exception as e:
            print(f"Error fetching letter {letter}: {e}")
            
        # Be nice to the API
        time.sleep(0.2)

    # Save to file (Overwriting old one as requested)
    base_dir = os.getcwd()
    file_path = os.path.join(base_dir, "backend/data/recipes.json")
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, "w") as f:
        json.dump(new_recipes, f, indent=4)
        
    print(f"DONE! Saved {len(new_recipes)} unique recipes to {file_path}")

if __name__ == "__main__":
    generate_bulk_dataset(500)
