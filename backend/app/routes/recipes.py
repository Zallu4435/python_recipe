
from typing import Optional
from fastapi import APIRouter, HTTPException
from backend.app.models.schemas import RecipeDetail, ValidationRequest, ValidationResponse, PaginatedSearchResponse
from backend.app.services.recipe_service import search_recipes_logic, validate_plan_logic
from backend.app.database.db import get_recipe_by_id

router = APIRouter()

@router.get("/search", response_model=PaginatedSearchResponse)
def search_recipes(q: Optional[str] = "", page: int = 1, limit: int = 12, category: Optional[str] = None):
    results, total = search_recipes_logic(q, page, limit, category)
    
    total_pages = (total + limit - 1) // limit
    
    items = [
        {"id": r["id"], "name": r["name"], "image": r["image"]} 
        for r in results
    ]
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "size": limit,
        "totalPages": total_pages
    }

@router.get("/{recipe_id}", response_model=RecipeDetail)
def get_recipe(recipe_id: int):
    recipe = get_recipe_by_id(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    return {
        "id": recipe["id"],
        "name": recipe["name"],
        "image": recipe["image"],
        "hints": recipe["hints"]
    }

@router.post("/validate", response_model=ValidationResponse)
async def validate_recipe(req: ValidationRequest):
    result = await validate_plan_logic(req)
    if not result:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return result
