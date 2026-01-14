
import json
import os
from typing import List, Optional

# Global variable to simulate database
_RECIPES_DB = []

def load_db():
    global _RECIPES_DB
    try:
        # Construct absolute path to ensure we find the file from anywhere
        base_dir = os.getcwd()
        file_path = os.path.join(base_dir, "backend/data/recipes.json")
        
        with open(file_path, "r") as f:
            _RECIPES_DB = json.load(f)
        print(f"Database loaded: {len(_RECIPES_DB)} recipes.")
    except FileNotFoundError:
        print(f"Error: Database file not found at {file_path}")
        _RECIPES_DB = []

def get_all_recipes() -> List[dict]:
    return _RECIPES_DB

def get_recipe_by_id(recipe_id: int) -> Optional[dict]:
    return next((r for r in _RECIPES_DB if r["id"] == recipe_id), None)
