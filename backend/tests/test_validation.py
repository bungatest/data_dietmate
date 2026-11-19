from app.schemas.nutrition import (
    DayValidationInput,
    MealValidationItem,
    TargetNutritionInput,
)
from app.services.validation_service import RecipeData, validate_meal_plan


def _sample_recipes() -> dict[str, RecipeData]:
    return {
        "RCP_SAFE_1": RecipeData(
            recipe_id="RCP_SAFE_1",
            nama_masakan="Ayam Panggang Brokoli",
            kalori_kkal=500.0,
            karbohidrat_g=60.0,
            protein_g=30.0,
            lemak_g=15.0,
            bahan_bahan="- 150 gram dada ayam - 100 gram brokoli - 100 gram nasi putih",
        ),
        "RCP_SAFE_2": RecipeData(
            recipe_id="RCP_SAFE_2",
            nama_masakan="Tumis Labu Siam",
            kalori_kkal=500.0,
            karbohidrat_g=65.0,
            protein_g=20.0,
            lemak_g=18.0,
            bahan_bahan="- 200 gram labu siam - 2 siung bawang putih",
        ),
        "RCP_UDANG": RecipeData(
            recipe_id="RCP_UDANG",
            nama_masakan="Dimsum Ayam Udang",
            kalori_kkal=1000.0,
            karbohidrat_g=125.0,
            protein_g=50.0,
            lemak_g=33.0,
            bahan_bahan="- 100 gram udang - 200 gram paha ayam",
        ),
        "RCP_EGG_EN": RecipeData(
            recipe_id="RCP_EGG_EN",
            nama_masakan="Toge Telur",
            kalori_kkal=400.0,
            karbohidrat_g=40.0,
            protein_g=25.0,
            lemak_g=15.0,
            bahan_bahan="- 1 besar egg - 150 gram sprouts",
        ),
        "RCP_NULL_NUTRITION": RecipeData(
            recipe_id="RCP_NULL_NUTRITION",
            nama_masakan="Sup Bening",
            kalori_kkal=200.0,
            karbohidrat_g=None,
            protein_g=10.0,
            lemak_g=0.0,
            bahan_bahan="- 100 gram wortel - 500 ml air",
        ),
    }


def _default_target() -> TargetNutritionInput:
    return TargetNutritionInput(
        target_calories=2000.0,
        carbs_g=250.0,
        protein_g=100.0,
        fat_g=66.67,
    )


def test_allergen_hard_constraint():
    """Resep dengan alergen HARUS ditolak meskipun kalori sesuai target."""
    recipes = _sample_recipes()
    days = [
        DayValidationInput(
            day=1,
            meals=[
                MealValidationItem(
                    recipe_id="RCP_UDANG",
                    recipe_name="Dimsum Ayam Udang",
                    servings=2.0,
                    meal_type="lunch",
                )
            ],
        )
    ]

    result = validate_meal_plan(
        days=days,
        recipes_by_id=recipes,
        target_nutrition=_default_target(),
        allergies=["udang"],
    )
    assert result.is_valid is False
    assert result.status == "failed"
    assert result.rejection_reason is not None
    assert "allergen" in result.rejection_reason.lower()


def test_allergen_synonym_text_matching():
    """Pencocokan alergen 'telur' juga harus mendeteksi kata 'egg' di bahan_bahan."""
    recipes = _sample_recipes()
    days = [
        DayValidationInput(
            day=1,
            meals=[MealValidationItem(recipe_id="RCP_EGG_EN", servings=1.0, meal_type="breakfast")],
        )
    ]
    result = validate_meal_plan(
        days=days,
        recipes_by_id=recipes,
        target_nutrition=_default_target(),
        allergies=["telur"],
    )
    assert result.is_valid is False
    assert result.status == "failed"
    assert result.rejection_reason is not None
    assert "allergen" in result.rejection_reason.lower()


def test_missing_recipe_id_rejected():
    recipes = _sample_recipes()
    days = [
        DayValidationInput(
            day=1,
            meals=[MealValidationItem(recipe_id="RCP_NONEXISTENT", servings=1.0, meal_type="lunch")],
        )
    ]
    result = validate_meal_plan(
        days=days,
        recipes_by_id=recipes,
        target_nutrition=_default_target(),
    )
    assert result.is_valid is False
    assert result.status == "failed"
    assert "RCP_NONEXISTENT" in (result.rejection_reason or "")


def test_invalid_servings_rejected():
    recipes = _sample_recipes()
    days = [
        DayValidationInput(
            day=1,
            meals=[
                MealValidationItem(recipe_id="RCP_SAFE_1", servings=0.0, meal_type="lunch"),
                MealValidationItem(recipe_id="RCP_SAFE_2", servings=12.0, meal_type="dinner"),
            ],
        )
    ]
    result = validate_meal_plan(
        days=days,
        recipes_by_id=recipes,
        target_nutrition=_default_target(),
    )
    assert result.is_valid is False
    assert len(result.hard_violations) == 2


def test_valid_meal_plan_within_tolerance():
    recipes = _sample_recipes()
    # 2 * 500 + 2 * 500 = 2000 kcal; carbs=250g; protein=100g; fat=66g (dalam ±10%)
    days = [
        DayValidationInput(
            day=1,
            meals=[
                MealValidationItem(recipe_id="RCP_SAFE_1", servings=2.0, meal_type="lunch"),
                MealValidationItem(recipe_id="RCP_SAFE_2", servings=2.0, meal_type="dinner"),
            ],
        )
    ]
    result = validate_meal_plan(
        days=days,
        recipes_by_id=recipes,
        target_nutrition=_default_target(),
        allergies=["udang"],
    )
    assert result.is_valid is True
    assert result.status == "valid"
    assert result.within_tolerance is True
    assert result.total_actual_nutrition.calories == 2000.0


def test_soft_constraint_calorie_deviation_and_recipe_repetition():
    recipes = _sample_recipes()
    # Muncul 3 kali (melebihi max 2 kali) dan total kalori menyimpang > 10%
    days = [
        DayValidationInput(
            day=1,
            meals=[MealValidationItem(recipe_id="RCP_SAFE_1", servings=1.0, meal_type="lunch")],
        ),
        DayValidationInput(
            day=2,
            meals=[MealValidationItem(recipe_id="RCP_SAFE_1", servings=1.0, meal_type="lunch")],
        ),
        DayValidationInput(
            day=3,
            meals=[MealValidationItem(recipe_id="RCP_SAFE_1", servings=1.0, meal_type="lunch")],
        ),
    ]
    result = validate_meal_plan(
        days=days,
        recipes_by_id=recipes,
        target_nutrition=_default_target(),
        max_recipe_repeats=2,
    )
    assert result.is_valid is True
    assert result.status == "adjusted"
    assert result.within_tolerance is False
    assert any("pengulangan" in msg.lower() for msg in result.soft_violations)


def test_incomplete_nutrition_adds_warning():
    recipes = _sample_recipes()
    days = [
        DayValidationInput(
            day=1,
            meals=[MealValidationItem(recipe_id="RCP_NULL_NUTRITION", servings=1.0, meal_type="lunch")],
        )
    ]
    result = validate_meal_plan(
        days=days,
        recipes_by_id=recipes,
        target_nutrition=_default_target(),
    )
    assert any("tidak lengkap" in w.lower() for w in result.warnings)

