from app.core.config import settings
from app.schemas.nutrition import MacroTargets, NutritionResult
from app.schemas.user import UserProfile
from app.services.bmi_service import calculate_bmi, get_bmi_category
from app.services.calorie_service import (
    calculate_bmr,
    calculate_target_calories,
    calculate_tdee,
    get_calorie_warnings,
)
from app.services.macro_service import (
    DEFAULT_CARBS_PCT,
    DEFAULT_FAT_PCT,
    DEFAULT_PROTEIN_PCT,
    calculate_macros,
)


def calculate_user_nutrition(profile: UserProfile) -> NutritionResult:
    """Menjalankan pipeline lengkap perhitungan BMI, BMR, TDEE, target kalori, dan makronutrien."""
    bmi = calculate_bmi(weight_kg=profile.weight_kg, height_cm=profile.height_cm)
    bmi_category = get_bmi_category(bmi=bmi, standard=settings.BMI_STANDARD)

    bmr = calculate_bmr(
        weight_kg=profile.weight_kg,
        height_cm=profile.height_cm,
        age=profile.age,
        gender=profile.gender,
    )
    tdee = calculate_tdee(bmr=bmr, activity_level=profile.activity_level)
    target_calories = calculate_target_calories(tdee=tdee, diet_goal=profile.diet_goal)
    warnings = get_calorie_warnings(target_calories=target_calories)

    if profile.macro_distribution is not None:
        carbs_pct = profile.macro_distribution.carbs_pct
        protein_pct = profile.macro_distribution.protein_pct
        fat_pct = profile.macro_distribution.fat_pct
    else:
        carbs_pct = DEFAULT_CARBS_PCT
        protein_pct = DEFAULT_PROTEIN_PCT
        fat_pct = DEFAULT_FAT_PCT

    macro_dict = calculate_macros(
        target_calories=target_calories,
        carbs_pct=carbs_pct,
        protein_pct=protein_pct,
        fat_pct=fat_pct,
    )

    return NutritionResult(
        bmi=round(bmi, 2),
        bmi_category=bmi_category,
        bmi_standard=settings.BMI_STANDARD,
        bmr=round(bmr, 2),
        tdee=round(tdee, 2),
        target_calories=round(target_calories, 2),
        macros=MacroTargets(**macro_dict),
        warnings=warnings,
    )

