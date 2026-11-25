from datetime import datetime, timezone
import re
import time
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
from app.services.generation_log_service import GenerationTrace, record_generation
from app.services.nutrition_service import calculate_user_nutrition
from app.services.profile_service import upsert_profile
from app.services.validation_service import (
    RecipeData,
    find_matching_allergens,
    recipe_from_orm,
    validate_meal_plan,
)

# Meal plan DietMate selalu terdiri dari 3 waktu makan per hari.
MEAL_SLOTS: tuple[str, ...] = ("breakfast", "lunch", "dinner")
MEALS_PER_DAY = len(MEAL_SLOTS)

# Distribusi energi harian per waktu makan (total 100%).
MEAL_SLOT_WEIGHTS: dict[str, float] = {
    "breakfast": 0.28,
    "lunch": 0.39,
    "dinner": 0.33,
}

# Kategori dataset (cleaned_recipes.csv) yang bukan makanan utama dan tidak dipakai di meal plan.
EXCLUDED_CATEGORIES: frozenset[str] = frozenset(
    {"minuman", "saus dan bumbu", "makanan penutup", "makanan ringan"}
)
PREFERRED_CATEGORIES: dict[str, frozenset[str]] = {
    "breakfast": frozenset({"makan pagi", "roti & produk panggang"}),
    "lunch": frozenset({"makan siang", "hidangan utama"}),
    "dinner": frozenset({"hidangan utama", "lauk pauk", "sup"}),
}

GOAL_MAPPING = {
    "weight_loss": "lose_weight",
    "maintenance": "maintain",
    "muscle_gain": "gain_muscle",
    "lose_weight": "lose_weight",
    "maintain": "maintain",
    "gain_muscle": "gain_muscle",
}

# Kode preferensi frontend (frontend/src/lib/constants.ts FOOD_PREFERENCE_OPTIONS)
PREF_VEGETARIAN = "vegetarian"
PREF_HIGH_PROTEIN = "high_protein"
PREF_LOW_SPICY = "low_spicy"
PREF_SIMPLE_MEALS = "simple_meals"
PREFERENCE_CODES = frozenset({PREF_VEGETARIAN, PREF_HIGH_PROTEIN, PREF_LOW_SPICY, PREF_SIMPLE_MEALS})

NON_VEGETARIAN_TERMS: tuple[str, ...] = (
    "ayam", "chicken", "daging", "sapi", "beef", "kambing", "mutton", "lamb", "babi", "pork",
    "bacon", "ham", "sosis", "sausage", "bakso", "kornet", "ati", "hati ayam", "ikan", "fish",
    "tuna", "salmon", "tenggiri", "tongkol", "lele", "patin", "teri", "bandeng", "kakap", "dori",
    "sarden", "nila", "udang", "shrimp", "prawn", "ebi", "cumi", "squid", "kerang", "clam",
    "kepiting", "crab", "tiram", "oyster", "lobster", "kalkun", "turkey", "bebek", "duck",
)
SPICY_TERMS: tuple[str, ...] = ("cabai", "cabe", "rawit", "sambal", "pedas", "chili", "chilli", "jalapeno")
SIMPLE_MEAL_MAX_INGREDIENTS = 6


def _contains_any(text: str, terms: tuple[str, ...]) -> bool:
    return any(re.search(rf"\b{re.escape(term)}\b", text) for term in terms)


def _split_ingredients(text: str | None) -> list[str]:
    """Memecah bahan dengan format dataset '- 1 sdm a - 2 g b' (juga mendukung baris baru / ';')."""
    if not text:
        return []
    items = re.split(r"[\n;]+|(?:^|\s)-\s+", text)
    return [item.strip(" -") for item in items if item and item.strip(" -")]


def _split_instructions(text: str | None) -> list[str]:
    """Memecah langkah masak dengan format dataset '1. ... 2. ...' (juga mendukung baris baru / ';')."""
    if not text:
        return []
    items = re.split(r"[\n;]+|(?:^|\s)\d+[\.\)]\s+", text)
    return [item.strip() for item in items if item and item.strip()]


def _build_recipe_detail(recipe: Recipe) -> RecipeDetail:
    """Membentuk objek RecipeDetail lengkap untuk halaman resep frontend."""
    ingredients = _split_ingredients(recipe.bahan_bahan)
    instructions = _split_instructions(recipe.cara_memasak)
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


def _recipe_haystack(recipe: RecipeData) -> str:
    return f"{recipe.nama_masakan} {recipe.bahan_bahan or ''}".lower()


def _is_allowed_by_preferences(recipe: RecipeData, preferences: list[str]) -> bool:
    """Preferensi yang bersifat pembatasan (mis. vegetarian) diperlakukan sebagai filter."""
    normalized = {p.strip().lower() for p in preferences}
    if PREF_VEGETARIAN in normalized and _contains_any(_recipe_haystack(recipe), NON_VEGETARIAN_TERMS):
        return False
    return True


def _preference_score(recipe: RecipeData, preferences: list[str]) -> float:
    """Skor kecocokan preferensi: kode preferensi frontend + kata bahan bebas (mis. 'ayam')."""
    if not preferences:
        return 0.0
    haystack = _recipe_haystack(recipe)
    score = 0.0
    for raw in preferences:
        pref = raw.strip().lower()
        if not pref or pref == PREF_VEGETARIAN:
            continue
        if pref == PREF_HIGH_PROTEIN:
            kcal = float(recipe.kalori_kkal or 0.0)
            protein = float(recipe.protein_g or 0.0)
            # >= 25% energi dari protein dianggap tinggi protein
            if kcal > 0 and (protein * 4.0) / kcal >= 0.25:
                score += 1.0
        elif pref == PREF_LOW_SPICY:
            if not _contains_any(haystack, SPICY_TERMS):
                score += 1.0
        elif pref == PREF_SIMPLE_MEALS:
            if len(_split_ingredients(recipe.bahan_bahan)) <= SIMPLE_MEAL_MAX_INGREDIENTS:
                score += 1.0
        elif pref not in PREFERENCE_CODES and pref in haystack:
            score += 1.0
    return score


def _normalize_category(kategori: str | None) -> str:
    return (kategori or "").strip().lower()


def _is_category_allowed(kategori: str | None) -> bool:
    return _normalize_category(kategori) not in EXCLUDED_CATEGORIES


def _slot_calorie_targets(daily_calories: float) -> list[float]:
    return [daily_calories * MEAL_SLOT_WEIGHTS[slot] for slot in MEAL_SLOTS]


def _estimate_servings(recipe: RecipeData, target_meal_calories: float) -> float:
    kcal = float(recipe.kalori_kkal or 0.0)
    if kcal <= 0:
        return 1.0
    raw = target_meal_calories / kcal
    rounded = round(raw * 2.0) / 2.0
    return max(0.5, min(4.0, rounded))


def _extract_user_profile_and_options(
    request: UnifiedMealPlanRequest,
) -> tuple[UserProfile, int]:
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
        return profile, duration

    if request.user_profile is not None:
        return request.user_profile, request.duration_days

    raise ValueError("Request harus menyertakan data 'profile'.")


def _build_slot_pools(
    safe_recipes: list[RecipeData],
    category_by_id: dict[str, str | None],
    slot_targets: list[float],
    preferences: list[str],
) -> dict[str, list[RecipeData]]:
    """Menyusun kandidat resep terurut per waktu makan."""
    pools: dict[str, list[RecipeData]] = {}
    for slot, target in zip(MEAL_SLOTS, slot_targets):
        candidates = [r for r in safe_recipes if _is_category_allowed(category_by_id.get(r.recipe_id))]
        if not candidates:
            # Fallback: dataset tidak punya kategori yang cocok, gunakan semua resep aman.
            candidates = list(safe_recipes)
        preferred = PREFERRED_CATEGORIES.get(slot, frozenset())
        candidates.sort(
            key=lambda r, t=target, p=preferred: (
                -_preference_score(r, preferences),
                0 if _normalize_category(category_by_id.get(r.recipe_id)) in p else 1,
                abs(float(r.kalori_kkal or 0.0) - t),
                r.recipe_id,
            )
        )
        pools[slot] = candidates
    return pools


def generate_meal_plan(
    db: Session,
    request: UnifiedMealPlanRequest,
    user_id: str | None = None,
) -> MealPlanResponse:
    """Titik masuk generate meal plan: simpan profil, jalankan generator, catat generation_logs.

    Saat RAG tersedia (Phase 3), generator RAG dipanggil di sini dengan fallback ke stub.
    """
    request_payload = request.model_dump(mode="json", exclude_none=True)
    trace = GenerationTrace(source="stub")
    started = time.perf_counter()

    def _elapsed_ms() -> int:
        return int((time.perf_counter() - started) * 1000)

    try:
        if user_id is not None and request.profile is not None:
            # Profil & preferensi terakhir yang dipakai generate selalu tersimpan di user_profiles.
            upsert_profile(db, user_id, request.profile, request.preferences, commit=False)
        response = generate_meal_plan_stub(db, request, user_id=user_id, trace=trace)
    except Exception as exc:
        db.rollback()
        record_generation(
            db,
            trace=trace,
            status="failed",
            request_payload=request_payload,
            latency_ms=_elapsed_ms(),
            user_id=user_id,
            error_message=f"{type(exc).__name__}: {exc}",
        )
        raise

    record_generation(
        db,
        trace=trace,
        status="success",
        request_payload=request_payload,
        latency_ms=_elapsed_ms(),
        user_id=user_id,
        plan_id=response.plan_id,
        validation_passed=response.validation.passed,
        validation_warnings=response.validation.warnings,
    )
    return response


def generate_meal_plan_stub(
    db: Session,
    request: UnifiedMealPlanRequest,
    user_id: str | None = None,
    trace: GenerationTrace | None = None,
) -> MealPlanResponse:
    """Menyusun rekomendasi meal plan dari database resep (tanpa LLM)."""
    user_profile, duration_days = _extract_user_profile_and_options(request)
    user_target = calculate_user_nutrition(user_profile)

    all_recipes = db.query(Recipe).order_by(Recipe.recipe_id.asc()).all()
    if not all_recipes:
        raise LookupError("Tabel 'recipes' di database kosong. Harap load resep terlebih dahulu.")

    orm_recipe_map = {r.recipe_id: r for r in all_recipes}
    recipe_map = {r.recipe_id: recipe_from_orm(r) for r in all_recipes}
    category_by_id = {r.recipe_id: r.kategori for r in all_recipes}

    safe_recipes = [
        data
        for data in recipe_map.values()
        if not find_matching_allergens(data, user_profile.allergies)
        and _is_allowed_by_preferences(data, user_profile.preferences)
        and (data.kalori_kkal or 0.0) > 0
    ]

    if not safe_recipes:
        raise LookupError(
            "Tidak ditemukan resep yang aman dan sesuai untuk daftar alergi/preferensi pengguna."
        )

    slot_targets = _slot_calorie_targets(user_target.target_calories)
    pools = _build_slot_pools(safe_recipes, category_by_id, slot_targets, user_profile.preferences)
    cursors: dict[str, int] = {slot: 0 for slot in pools}
    usage_counter: dict[str, int] = {r.recipe_id: 0 for r in safe_recipes}
    max_repeats = settings.MAX_RECIPE_REPEATS

    validation_days: list[DayValidationInput] = []
    unified_days: list[MealPlanDay] = []

    for day_num in range(1, duration_days + 1):
        planned_meals: list[PlannedMeal] = []
        day_val_items: list[MealValidationItem] = []
        used_today: set[str] = set()

        for slot, target_meal_cal in zip(MEAL_SLOTS, slot_targets):
            pool = pools[slot]
            total_pool = len(pool)
            cursor = cursors[slot]
            chosen: RecipeData | None = None
            for offset in range(total_pool):
                candidate = pool[(cursor + offset) % total_pool]
                if (
                    usage_counter[candidate.recipe_id] < max_repeats
                    and candidate.recipe_id not in used_today
                ):
                    chosen = candidate
                    cursors[slot] = (cursor + offset + 1) % total_pool
                    break

            if chosen is None:
                chosen = pool[cursor % total_pool]
                cursors[slot] = (cursor + 1) % total_pool

            usage_counter[chosen.recipe_id] += 1
            used_today.add(chosen.recipe_id)
            if trace is not None:
                trace.selected_recipe_ids.append(chosen.recipe_id)
            servings = _estimate_servings(chosen, target_meal_cal)

            orm_rec = orm_recipe_map[chosen.recipe_id]
            recipe_detail = _build_recipe_detail(orm_rec)

            meal_nutrition = NutritionValues(
                calories_kcal=round(float(chosen.kalori_kkal or 0.0) * servings, 1),
                protein_g=round(float(chosen.protein_g or 0.0) * servings, 1),
                carbs_g=round(float(chosen.karbohidrat_g or 0.0) * servings, 1),
                fat_g=round(float(chosen.lemak_g or 0.0) * servings, 1),
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
    # created_at diisi dari aplikasi (presisi mikrodetik) agar urutan "plan terbaru" selalu pasti.
    created_at = datetime.now(timezone.utc)
    now_iso = created_at.isoformat()
    source = "stub"

    response = MealPlanResponse(
        plan_id=plan_id,
        source=source,
        generated_at=now_iso,
        nutrition_summary=_build_nutrition_summary(user_target),
        days=unified_days,
        validation=ValidationSummary(
            passed=validation.is_valid,
            warnings=combined_warnings,
        ),
    )

    # Simpan ke tabel meal_plans di database
    db_record = MealPlan(
        plan_id=plan_id,
        user_id=user_id,
        source=source,
        user_profile=user_profile.model_dump(),
        user_target=user_target.model_dump(),
        duration_days=duration_days,
        meals_per_day=MEALS_PER_DAY,
        days=[d.model_dump() for d in unified_days],
        validation_status=validation.status,
        warnings=combined_warnings,
        created_at=created_at,
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)

    return response


def _build_nutrition_summary(user_target: NutritionResult) -> NutritionSummary:
    return NutritionSummary(
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


def get_latest_meal_plan(db: Session, user_id: str) -> MealPlanResponse | None:
    """Meal plan terbaru milik user (dipakai frontend untuk memulihkan dashboard setelah login)."""
    record = (
        db.query(MealPlan)
        .filter(MealPlan.user_id == user_id)
        .order_by(MealPlan.created_at.desc(), MealPlan.plan_id.desc())
        .first()
    )
    if record is None:
        return None
    return get_meal_plan_by_id(db, record.plan_id, user_id)


def get_meal_plan_by_id(
    db: Session,
    plan_id: str,
    user_id: str | None = None,
) -> MealPlanResponse | None:
    """Mengambil meal plan berdasarkan id. Plan milik user lain diperlakukan sebagai tidak ditemukan."""
    record = db.query(MealPlan).filter(MealPlan.plan_id == plan_id).first()
    if record is None:
        return None
    if record.user_id is not None and record.user_id != user_id:
        return None

    user_target = NutritionResult.model_validate(record.user_target)
    parsed_days = [MealPlanDay.model_validate(d) for d in record.days]

    return MealPlanResponse(
        plan_id=record.plan_id,
        source=record.source or "stub",
        generated_at=record.created_at.isoformat() if record.created_at else "",
        nutrition_summary=_build_nutrition_summary(user_target),
        days=parsed_days,
        validation=ValidationSummary(
            passed=record.validation_status in ("valid", "adjusted"),
            warnings=list(record.warnings or []),
        ),
    )
