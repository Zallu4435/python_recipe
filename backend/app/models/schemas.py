
from typing import List
from pydantic import BaseModel

class RecipeSchema(BaseModel):
    id: int
    name: str
    image: str
    ingredients: List[str]
    hints: List[str]

class SearchResponse(BaseModel):
    id: int
    name: str
    image: str

class PaginatedSearchResponse(BaseModel):
    items: List[SearchResponse]
    total: int
    page: int
    size: int
    totalPages: int

class RecipeDetail(BaseModel):
    id: int
    name: str
    image: str
    hints: List[str]

class ValidationRequest(BaseModel):
    recipe_id: int
    plan: str
    hints_used: int

class ValidationResponse(BaseModel):
    score: int
    feedback: str
    matched_ingredients: List[str]
    all_ingredients: List[str]
