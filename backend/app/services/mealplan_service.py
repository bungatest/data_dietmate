from datetime import datetime, timezone
import re
from uuid import uuid4

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.meal_plan import MealPlan
from app.models.recipe import Recipe
from app.schemas.mealplan import (
    MealPlanDay,
    MealPlanResponse,
    NutritionSummary,
    NutritionValues,
    PlannedMeal,
    RecipeDetail,
    UnifiedMealPlanRequest,
    ValidationSummary,
)
from app.schemas.nutrition import (
    DayValidationInput,
    MealValidationItem,
    NutritionResult,
    TargetNutritionInput,
)
from app.schemas.user import UserProfile
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

GOAL_MAPPING = {
    "weight_loss": "lose_weight",
    "maintenance": "maintain",
    "muscle_gain": "gain_muscle",
    "lose_weight": "lose_weight",
    "maintain": "maintain",
    "gain_muscle": "gain_muscle",
}


def _split_text_items(text: str | None) -> list[str]:
    """Memecah teks bahan-bahan atau langkah masak menjadi list item bersih."""
    if not text:
        return []
    items = re.split(r"[\n;]+", text)
    cleaned = [re.sub(r"^\d+[\.\)]\s*", "", item).strip() for item in items]
    return [c for c in cleaned if c]


def _build_recipe_detail(recipe: Recipe) -> RecipeDetail:
    """Membentuk objek RecipeDetail lengkap untuk halaman resep frontend."""
    ingredients = _split_text_items(recipe.bahan_bahan)
    instructions = _split_text_items(recipe.cara_memasak)
    tags = [recipe.kategori.strip()] if recipe.kategori else ["Sehat"]

    return RecipeDetail(
        id=recipe.recipe_id,
        name=recipe.nama_masakan,
        description=f"Resep lezat dan bergizi {recipe.nama_masakan}",
        prep_time_minutes=20,
        servings=recipe.jumlah_porsi or 1,
        ingredients=ingredients or ["Bahan makanan segar sesuai takaran porsi"],
        instructions=instructions or ["Masak hingga matang dan sajikan hangat."],
        tags=tags,
    )


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
    rounded = round(raw * 2.0) / 2.0
    return max(0.5, min(4.0, rounded))


def _extract_user_profile_and_options(
    request: UnifiedMealPlanRequest,
) -> tuple[UserProfile, int, int]:
    """Mengekstrak data UserProfile dari payload frontend."""
    if request.profile is not None:
        raw_goal = request.preferences.goal if request.preferences else "maintenance"
        diet_goal = GOAL_MAPPING.get(raw_goal, "maintain")
        allergies = request.preferences.allergies if request.preferences else []
        preferences = request.preferences.food_preferences if request.preferences else []
        duration = request.preferences.duration_days if request.preferences else request.duration_days

        profile = UserProfile(
            age=request.profile.age,
            gender=request.profile.gender,
            weight_kg=request.profile.weight_kg,
            height_cm=request.profile.height_cm,
            activity_level=request.profile.activity_level,
            diet_goal=diet_goal,  # type: ignore[arg-type]
            allergies=allergies,
            preferences=preferences,
        )
        return profile, duration, request.meals_per_day

    if request.user_profile is not None:
        return request.user_profile, request.duration_days, request.meals_per_day

    raise ValueError("Request harus menyertakan data 'profile'.")


def generate_meal_plan_stub(db: Session, request: UnifiedMealPlanRequest) -> MealPlanResponse:
    """Menyusun rekomendasi meal plan dari database resep."""
    user_profile, duration_days, meals_per_day = _extract_user_profile_and_options(request)
    user_target = calculate_user_nutrition(user_profile)

    all_recipes = db.query(Recipe).order_by(Recipe.recipe_id.asc()).all()
    if not all_recipes:
        raise LookupError("Tabel 'recipes' di database kosong. Harap load resep terlebih dahulu.")

    orm_recipe_map = {r.recipe_id: r for r in all_recipes}
    recipe_map = {r.recipe_id: recipe_from_orm(r) for r in all_recipes}

    safe_recipes = [
        data
        for data in recipe_map.values()
        if not find_matching_allergens(data, user_profile.allergies)
        and (data.kalori_kkal or 0.0) > 0
    ]

    if not safe_recipes:
        raise LookupError("Tidak ditemukan resep yang aman dan sesuai untuk daftar alergi pengguna.")

    target_meal_cal = user_target.target_calories / meals_per_day
    safe_recipes.sort(
        key=lambda r: (
            -_preference_score(r, user_profile.preferences),
            abs(float(r.kalori_kkal or 0.0) - target_meal_cal),
            r.recipe_id,
        )
    )

    meal_slots = MEAL_SLOT_SEQUENCES.get(meals_per_day, ["breakfast", "lunch", "dinner"])
    usage_counter: dict[str, int] = {r.recipe_id: 0 for r in safe_recipes}
    max_repeats = settings.MAX_RECIPE_REPEATS

    validation_days: list[DayValidationInput] = []
    unified_days: list[MealPlanDay] = []
    cursor = 0
    total_pool = len(safe_recipes)

    for day_num in range(1, duration_days + 1):
        planned_meals: list[PlannedMeal] = []
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

            orm_rec = orm_recipe_map[chosen.recipe_id]
            recipe_detail = _build_recipe_detail(orm_rec)

            meal_cal = round(float(chosen.kalori_kkal or 0.0) * servings, 1)
            meal_prot = round(float(chosen.protein_g or 0.0) * servings, 1)
            meal_carb = round(float(chosen.karbohidrat_g or 0.0) * servings, 1)
            meal_fat = round(float(chosen.lemak_g or 0.0) * servings, 1)

            meal_nutrition = NutritionValues(
                calories_kcal=meal_cal,
                protein_g=meal_prot,
                carbs_g=meal_carb,
                fat_g=meal_fat,
            )

            planned_meals.append(
                PlannedMeal(
                    meal_type=slot,  # type: ignore[arg-type]
                    servings=servings,
                    recipe=recipe_detail,
                    nutrition=meal_nutrition,
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
        unified_days.append(
            MealPlanDay(
                day_number=day_num,
                meals=planned_meals,
                totals=NutritionValues(calories_kcal=0, protein_g=0, carbs_g=0, fat_g=0),
            )
        )

    # Validasi hard & soft constraint
    validation = validate_meal_plan(
        days=validation_days,
        recipes_by_id=recipe_map,
        target_nutrition=TargetNutritionInput(
            target_calories=user_target.target_calories,
            carbs_g=user_target.macros.carbs_g,
            protein_g=user_target.macros.protein_g,
            fat_g=user_target.macros.fat_g,
        ),
        allergies=user_profile.allergies,
    )

    for day_plan, summary in zip(unified_days, validation.daily_summaries):
        day_plan.totals.calories_kcal = summary.actual.calories
        day_plan.totals.carbs_g = summary.actual.carbs_g
        day_plan.totals.protein_g = summary.actual.protein_g
        day_plan.totals.fat_g = summary.actual.fat_g

    combined_warnings = list(user_target.warnings) + list(validation.warnings)
    plan_id = f"MP_{uuid4().hex[:12]}"
    now_iso = datetime.now(timezone.utc).isoformat()

    nutrition_summary = NutritionSummary(
        calories_kcal=user_target.target_calories,
        protein_g=user_target.macros.protein_g,
        carbs_g=user_target.macros.carbs_g,
        fat_g=user_target.macros.fat_g,
        bmi=user_target.bmi,
        bmi_category=user_target.bmi_category,
        bmr_kcal=user_target.bmr,
        tdee_kcal=user_target.tdee,
        target_calories_kcal=user_target.target_calories,
    )

    response = MealPlanResponse(
        plan_id=plan_id,
        source="stub",
        generated_at=now_iso,
        nutrition_summary=nutrition_summary,
        days=unified_days,
        validation=ValidationSummary(
            passed=validation.is_valid,
            warnings=combined_warnings,
        ),
    )

    # Simpan ke tabel meal_plans di database
    db_record = MealPlan(
        plan_id=plan_id,
        user_profile=user_profile.model_dump(),
        user_target=user_target.model_dump(),
        duration_days=duration_days,
        meals_per_day=meals_per_day,
        days=[d.model_dump() for d in unified_days],
        validation_status=validation.status,
        warnings=combined_warnings,
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)

    return response


def get_meal_plan_by_id(db: Session, plan_id: str) -> MealPlanResponse | None:
    """Mengambil meal plan berdasarkan id dari tabel database."""
    record = db.query(MealPlan).filter(MealPlan.plan_id == plan_id).first()
    if record is None:
        return None

    user_target = NutritionResult.model_validate(record.user_target)
    nutrition_summary = NutritionSummary(
        calories_kcal=user_target.target_calories,
        protein_g=user_target.macros.protein_g,
        carbs_g=user_target.macros.carbs_g,
        fat_g=user_target.macros.fat_g,
        bmi=user_target.bmi,
        bmi_category=user_target.bmi_category,
        bmr_kcal=user_target.bmr,
        tdee_kcal=user_target.tdee,
        target_calories_kcal=user_target.target_calories,
    )

    parsed_days = [MealPlanDay.model_validate(d) for d in record.days]

    return MealPlanResponse(
        plan_id=record.plan_id,
        source="stub",
        generated_at=record.created_at.isoformat() if record.created_at else "",
        nutrition_summary=nutrition_summary,
        days=parsed_days,
        validation=ValidationSummary(
            passed=record.validation_status in ("valid", "adjusted"),
            warnings=list(record.warnings or []),
        ),
    )