from uuid import uuid4

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.meal_plan import MealPlan
from app.models.recipe import Recipe
from app.schemas.mealplan import DayPlan, MealItem, MealPlanRequest, MealPlanResponse
from app.schemas.nutrition import (
    DayValidationInput,
    MealValidationItem,
    NutritionResult,
    TargetNutritionInput,
)
from app.services.nutrition_service import calculate_user_nutrition
from app.services.validation_service import (
    RecipeData,
    find_matching_allergens,
    recipe_from_orm,
    validate_meal_plan,
)

MEAL_SLOT_SEQUENCES: dict[int, list[str]] = {
    1: ["lunch"],
    2: ["breakfast", "dinner"],
    3: ["breakfast", "lunch", "dinner"],
    4: ["breakfast", "lunch", "snack", "dinner"],
    5: ["breakfast", "snack", "lunch", "snack", "dinner"],
}


def _preference_score(recipe: RecipeData, preferences: list[str]) -> int:
    if not preferences:
        return 0
    haystack = f"{recipe.nama_masakan} {recipe.bahan_bahan or ''}".lower()
    return sum(1 for pref in preferences if pref.strip() and pref.strip().lower() in haystack)


def _estimate_servings(recipe: RecipeData, target_meal_calories: float) -> float:
    kcal = float(recipe.kalori_kkal or 0.0)
    if kcal <= 0:
        return 1.0
    raw = target_meal_calories / kcal
    # Bulatkan ke kelipatan 0.5 terdekat dengan batas wajar 0.5–4.0 porsi per sajian
    rounded = round(raw * 2.0) / 2.0
    return max(0.5, min(4.0, rounded))


def generate_meal_plan_stub(db: Session, request: MealPlanRequest) -> MealPlanResponse:
    """Stub generator meal plan berbasis resep PostgreSQL, tervalidasi dan tersimpan ke tabel meal_plans."""
    user_target = calculate_user_nutrition(request.user_profile)

    all_recipes = db.query(Recipe).order_by(Recipe.recipe_id.asc()).all()
    if not all_recipes:
        raise LookupError("Tabel 'recipes' di database kosong. Jalankan notebook pengisian resep terlebih dahulu.")

    recipe_map = {r.recipe_id: recipe_from_orm(r) for r in all_recipes}
    safe_recipes = [
        data
        for data in recipe_map.values()
        if not find_matching_allergens(data, request.user_profile.allergies)
        and (data.kalori_kkal or 0.0) > 0
    ]

    if not safe_recipes:
        raise LookupError("Tidak ditemukan resep yang aman dan sesuai untuk daftar alergi pengguna.")

    # Urutkan berdasarkan kecocokan preferensi lalu kedekatan kalori per sajian
    target_meal_cal = user_target.target_calories / request.meals_per_day
    safe_recipes.sort(
        key=lambda r: (
            -_preference_score(r, request.user_profile.preferences),
            abs(float(r.kalori_kkal or 0.0) - target_meal_cal),
            r.recipe_id,
        )
    )

    meal_slots = MEAL_SLOT_SEQUENCES[request.meals_per_day]
    usage_counter: dict[str, int] = {r.recipe_id: 0 for r in safe_recipes}
    max_repeats = settings.MAX_RECIPE_REPEATS

    validation_days: list[DayValidationInput] = []
    response_days: list[DayPlan] = []

    cursor = 0
    total_pool = len(safe_recipes)

    for day_num in range(1, request.duration_days + 1):
        day_meals: list[MealItem] = []
        day_val_items: list[MealValidationItem] = []

        for slot in meal_slots:
            chosen: RecipeData | None = None
            for offset in range(total_pool):
                candidate = safe_recipes[(cursor + offset) % total_pool]
                if usage_counter[candidate.recipe_id] < max_repeats:
                    chosen = candidate
                    cursor = (cursor + offset + 1) % total_pool
                    break

            if chosen is None:
                chosen = safe_recipes[cursor % total_pool]
                cursor = (cursor + 1) % total_pool

            usage_counter[chosen.recipe_id] += 1
            servings = _estimate_servings(chosen, target_meal_cal)

            day_meals.append(
                MealItem(
                    recipe_id=chosen.recipe_id,
                    recipe_name=chosen.nama_masakan,
                    servings=servings,
                    meal_type=slot,  # type: ignore[arg-type]
                )
            )
            day_val_items.append(
                MealValidationItem(
                    recipe_id=chosen.recipe_id,
                    recipe_name=chosen.nama_masakan,
                    servings=servings,
                    meal_type=slot,  # type: ignore[arg-type]
                )
            )

        validation_days.append(DayValidationInput(day=day_num, meals=day_val_items))
        response_days.append(
            DayPlan(
                day=day_num,
                meals=day_meals,
                total_calories=0.0,
                total_carbs_g=0.0,
                total_protein_g=0.0,
                total_fat_g=0.0,
            )
        )

    validation = validate_meal_plan(
        days=validation_days,
        recipes_by_id=recipe_map,
        target_nutrition=TargetNutritionInput(
            target_calories=user_target.target_calories,
            carbs_g=user_target.macros.carbs_g,
            protein_g=user_target.macros.protein_g,
            fat_g=user_target.macros.fat_g,
        ),
        allergies=request.user_profile.allergies,
    )

    for day_plan, summary in zip(response_days, validation.daily_summaries):
        day_plan.total_calories = summary.actual.calories
        day_plan.total_carbs_g = summary.actual.carbs_g
        day_plan.total_protein_g = summary.actual.protein_g
        day_plan.total_fat_g = summary.actual.fat_g

    combined_warnings = list(user_target.warnings) + list(validation.warnings)
    combined_warnings.append(
        "Catatan: Meal plan ini dihasilkan oleh stub endpoint sementara sebelum integrasi penuh RAG/LLM."
    )

    plan_id = f"MP_{uuid4().hex[:12]}"
    db_record = MealPlan(
        plan_id=plan_id,
        user_profile=request.user_profile.model_dump(),
        user_target=user_target.model_dump(),
        duration_days=request.duration_days,
        meals_per_day=request.meals_per_day,
        days=[d.model_dump() for d in response_days],
        validation_status=validation.status,
        warnings=combined_warnings,
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)

    return MealPlanResponse(
        plan_id=db_record.plan_id,
        user_target=user_target,
        days=response_days,
        validation_status=validation.status,
        warnings=combined_warnings,
    )


def get_meal_plan_by_id(db: Session, plan_id: str) -> MealPlanResponse | None:
    """Mengambil data meal plan tersimpan dari tabel meal_plans berdasarkan plan_id."""
    record = db.query(MealPlan).filter(MealPlan.plan_id == plan_id).first()
    if record is None:
        return None

    return MealPlanResponse(
        plan_id=record.plan_id,
        user_target=NutritionResult.model_validate(record.user_target),
        days=[DayPlan.model_validate(d) for d in record.days],
        validation_status=record.validation_status,  # type: ignore[arg-type]
        warnings=list(record.warnings or []),
    )

