import os
import google.generativeai as genai
from dotenv import load_dotenv

# Ensure env is loaded here too
load_dotenv()

from typing import List, Optional
from backend.app.database.db import get_all_recipes, get_recipe_by_id
from backend.app.models.schemas import ValidationRequest, SearchResponse

# Configure Gemini
GENAI_API_KEY = os.getenv("GEMINI_API_KEY")
model = None

if GENAI_API_KEY:
    genai.configure(api_key=GENAI_API_KEY)
    # Using 'gemini-flash-latest' as it was explicitly listed in your available models
    model = genai.GenerativeModel('gemini-flash-latest')
else:
    print("Warning: GEMINI_API_KEY not set so AI features will be offline.")

def search_recipes_logic(query: str, page: int = 1, limit: int = 12, category: Optional[str] = None):
    recipes = get_all_recipes()
    
    filtered = recipes
    
    # Filter by text query
    if query:
        q = query.lower()
        filtered = [r for r in filtered if q in r["name"].lower()]
        
    # Filter by category
    if category and category != "All":
        filtered = [
            r for r in filtered 
            if any(h.startswith("Category: ") and h.split(": ")[1] == category for h in r.get("hints", []))
        ]

    # Total count after filter
    total = len(filtered)

    # Paginate
    start = (page - 1) * limit
    end = start + limit
    return filtered[start:end], total

async def validate_plan_logic(req: ValidationRequest):
    recipe = get_recipe_by_id(req.recipe_id)
    if not recipe:
        return None
    
    user_plan = req.plan.lower()
    ingredients = recipe["ingredients"]
    
    matched_ingredients = []
    for ing in ingredients:
        if ing.lower() in user_plan:
            matched_ingredients.append(ing)
    
    match_count = len(matched_ingredients)
    total_count = len(ingredients)
    
    # Proportional base score (0-100)
    base_score = (match_count / total_count) * 100
    
    # Hint penalty (reduced slightly to feel more balanced)
    hint_penalty = req.hints_used * 6
    
    # Final calculation
    score = base_score - hint_penalty
    
    # Perfection Bonus: If they got everything right with zero hints
    if match_count == total_count and req.hints_used == 0:
        score = 100
    
    score = max(5, min(100, round(score)))
    
    feedback = await generate_ai_feedback(recipe["name"], req.plan, score, matched_ingredients, ingredients)

    return {
        "score": score,
        "feedback": feedback,
        "matched_ingredients": matched_ingredients,
        "all_ingredients": ingredients
    }

async def generate_ai_feedback(recipe_name: str, plan: str, score: int, matched: List[str], all_ing: List[str]) -> str:
    if not model:
        return "Chef is out of the kitchen (Offline Mode). Your plan looks... functional."
    
    try:
        missed = list(set(all_ing) - set(matched))
        prompt = f"""
        Role: A legendary, hyper-critical Michelin-star Chef. 
        Context: Reviewing a student's cooking plan for '{recipe_name}'.
        
        Student's Plan: "{plan}"
        Score: {score}/100.
        Identified: {', '.join(matched) if matched else 'Absolutely nothing.'}
        Missing: {', '.join(missed[:5]) if missed else 'None! Perfect.'}.
        
        Format your response EXACTLY as follows (with labels):
        
        🔥 THE ROAST:
        [One savage, satirical sentence about their attempt.]
        
        👨‍🍳 THE CRITIQUE:
        [A one-sentence professional explanation of why they earned a {score}.]
        
        💡 THE CHEF'S SECRET:
        [One pro-level technical secret specifically about mastering {recipe_name}.]
        
        Tone: Brutal, expert, concise.
        """
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        error_msg = str(e)
        print(f"\n[AI ERROR] Failed to generate feedback: {error_msg}\n")  # Console log for backend debugging
        
        if "429" in error_msg or "Quota exceeded" in error_msg:
            return "Chef is overwhelmed with orders! (Rate Limit Hit - Try again in 30s) 🕒"
        if "404" in error_msg and "models/" in error_msg:
            return "Chef is on vacation (Model not found). Contact admin."
            
        return f"Chef is busy yelling at the sous-chef. (System Error: {error_msg[:50]}...)"
