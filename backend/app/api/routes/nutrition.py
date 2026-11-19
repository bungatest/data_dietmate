from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool

from app.api.dependencies import get_db
from app.models.recipe import Recipe
from app.schemas.nutrition import (
    MealPlanValidationRequest,
    NutritionResult,
    ValidationResult,
)
from app.schemas.user import UserProfile
from app.services.nutrition_service import calculate_user_nutrition
from app.services.validation_service import recipe_from_orm, validate_meal_plan

router = APIRouter(prefix="/nutrition", tags=["Nutrition"])


def _fetch_recipes_map(db: Session, recipe_ids: set[str]):
    if not recipe_ids:
        return {}
    rows = db.query(Recipe).filter(Recipe.recipe_id.in_(recipe_ids)).all()
    return {row.recipe_id: recipe_from_orm(row) for row in rows}


@router.post(
    "/calculate",
    response_model=NutritionResult,
    summary="Hitung BMI, BMR, TDEE, target kalori, dan makronutrien",
)
async def calculate_nutrition(profile: UserProfile) -> NutritionResult:
    """Menghitung kebutuhan nutrisi personal berdasarkan profil pengguna dan standar BMI aktif."""
    try:
        return calculate_user_nutrition(profile)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc


@router.post(
    "/validate",
    response_model=ValidationResult,
    summary="Validasi meal plan terhadap data nutrisi database dan alergen",
)
async def validate_nutrition(
    payload: MealPlanValidationRequest,
    db: Session = Depends(get_db),
) -> ValidationResult:
    """Memeriksa kebenaran recipe_id, jumlah porsi, alergen (hard constraint), dan deviasi nutrisi."""
    assert payload.days is not None
    requested_ids = {
        item.recipe_id
        for day in payload.days
        for item in day.meals
    }
    recipes_by_id = await run_in_threadpool(_fetch_recipes_map, db, requested_ids)

    return validate_meal_plan(
        days=payload.days,
        recipes_by_id=recipes_by_id,
        target_nutrition=payload.target_nutrition,
        allergies=payload.allergies,
        tolerance_pct=payload.tolerance_pct,
        max_recipe_repeats=payload.max_recipe_repeats,
    )

