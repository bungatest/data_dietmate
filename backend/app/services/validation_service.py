from collections import Counter
from dataclasses import dataclass, field
import re
from typing import Literal

from app.core.config import settings
from app.models.recipe import Recipe
from app.schemas.nutrition import (
    DayNutritionSummary,
    DayValidationInput,
    NutritionTotals,
    TargetNutritionInput,
    ValidationResult,
)

MAX_SERVINGS_PER_ITEM = 10.0

# Kelompok sinonim alergen lintas Bahasa Indonesia & Inggris untuk pencocokan teks pada bahan_bahan
ALLERGEN_SYNONYM_GROUPS: tuple[tuple[str, ...], ...] = (
    ("udang", "shrimp", "prawn", "ebi"),
    ("telur", "egg", "eggs", "putih telur", "kuning telur"),
    ("susu", "milk", "dairy", "keju", "cheese", "mozzarella", "cheddar", "parmesan", "yogurt", "yoghurt", "mentega", "butter", "krim", "cream", "whey"),
    ("kacang", "peanut", "peanuts", "kacang tanah", "almond", "mete", "cashew", "walnut", "kenari", "hazelnut", "pistachio"),
    ("kedelai", "soy", "soya", "soybean", "tahu", "tofu", "tempe", "tempeh", "kecap", "edamame"),
    ("ikan", "fish", "tuna", "salmon", "tenggiri", "tongkol", "lele", "patin", "teri", "bandeng", "kakap", "dori", "sarden"),
    ("seafood", "makanan laut", "udang", "shrimp", "prawn", "ikan", "fish", "cumi", "squid", "kerang", "clam", "kepiting", "crab", "tiram", "oyster", "lobster"),
    ("gluten", "gandum", "wheat", "terigu", "tepung terigu", "roti", "bread", "pasta", "mie", "spaghetti", "pangsit"),
    ("ayam", "chicken"),
    ("sapi", "daging sapi", "beef"),
)


@dataclass(frozen=True)
class RecipeData:
    """Representasi ringan data resep dari database untuk proses validasi murni."""

    recipe_id: str
    nama_masakan: str
    kalori_kkal: float | None
    karbohidrat_g: float | None
    protein_g: float | None
    lemak_g: float | None
    bahan_bahan: str | None = ""
    allergens: list[str] = field(default_factory=list)


def recipe_from_orm(recipe: Recipe) -> RecipeData:
    """Mengonversi model ORM Recipe menjadi RecipeData untuk service validasi."""
    return RecipeData(
        recipe_id=recipe.recipe_id,
        nama_masakan=recipe.nama_masakan,
        kalori_kkal=recipe.kalori_kkal,
        karbohidrat_g=recipe.karbohidrat_g,
        protein_g=recipe.protein_g,
        lemak_g=recipe.lemak_g,
        bahan_bahan=recipe.bahan_bahan or "",
    )


def _expand_allergen_terms(allergen: str) -> set[str]:
    normalized = allergen.strip().lower()
    if not normalized:
        return set()

    terms = {normalized}
    for group in ALLERGEN_SYNONYM_GROUPS:
        if normalized in group:
            terms.update(group)
    return terms


def find_matching_allergens(recipe: RecipeData, allergies: list[str]) -> list[str]:
    """Mencocokkan daftar alergen pengguna terhadap nama masakan, daftar bahan, dan metadata alergen."""
    if not allergies:
        return []

    haystack_parts = [
        recipe.nama_masakan or "",
        recipe.bahan_bahan or "",
        " ".join(recipe.allergens or []),
    ]
    haystack = " ".join(haystack_parts).lower()

    matched: list[str] = []
    for raw_allergen in allergies:
        clean_allergen = raw_allergen.strip()
        if not clean_allergen:
            continue

        terms = _expand_allergen_terms(clean_allergen)
        if any(re.search(rf"\b{re.escape(term)}\b", haystack) for term in terms):
            matched.append(clean_allergen)

    return matched


def has_incomplete_nutrition(recipe: RecipeData) -> bool:
    """Memeriksa apakah data nutrisi per porsi resep bernilai null atau <= 0."""
    fields = (recipe.kalori_kkal, recipe.karbohidrat_g, recipe.protein_g, recipe.lemak_g)
    return any(value is None or value <= 0 for value in fields)


def _calc_deviation_pct(actual: float, target: float) -> float:
    if target <= 0:
        return 0.0
    return round(((actual - target) / target) * 100.0, 2)


def validate_meal_plan(
    days: list[DayValidationInput],
    recipes_by_id: dict[str, RecipeData],
    target_nutrition: TargetNutritionInput,
    allergies: list[str] | None = None,
    tolerance_pct: float | None = None,
    max_recipe_repeats: int | None = None,
) -> ValidationResult:
    """Memvalidasi meal plan secara menyeluruh berdasarkan data resep terpercaya dari database."""
    user_allergies = allergies or []
    effective_tolerance = tolerance_pct if tolerance_pct is not None else settings.NUTRITION_TOLERANCE_PCT
    effective_max_repeats = max_recipe_repeats if max_recipe_repeats is not None else settings.MAX_RECIPE_REPEATS

    hard_violations: list[str] = []
    soft_violations: list[str] = []
    warnings: list[str] = []
    daily_summaries: list[DayNutritionSummary] = []

    recipe_usage_counts: Counter[str] = Counter()
    incomplete_flagged: set[str] = set()
    total_cal = total_carbs = total_protein = total_fat = 0.0

    for day_plan in days:
        day_cal = day_carbs = day_protein = day_fat = 0.0

        for item in day_plan.meals:
            recipe = recipes_by_id.get(item.recipe_id)
            if recipe is None:
                hard_violations.append(
                    f"Hari {day_plan.day}: recipe_id '{item.recipe_id}' tidak ditemukan di database."
                )
                continue

            if item.servings <= 0 or item.servings > MAX_SERVINGS_PER_ITEM:
                hard_violations.append(
                    f"Hari {day_plan.day}: jumlah porsi ({item.servings}) untuk '{item.recipe_id}' "
                    f"tidak valid (harus > 0 dan <= {int(MAX_SERVINGS_PER_ITEM)})."
                )
                continue

            matched_allergens = find_matching_allergens(recipe, user_allergies)
            if matched_allergens:
                allergen_list = ", ".join(matched_allergens)
                hard_violations.append(
                    f"Hari {day_plan.day}: hard constraint violated — allergen ({allergen_list}) "
                    f"terdeteksi pada resep '{recipe.recipe_id}' ({recipe.nama_masakan})."
                )

            if recipe.recipe_id not in incomplete_flagged and has_incomplete_nutrition(recipe):
                incomplete_flagged.add(recipe.recipe_id)
                warnings.append(
                    f"Data nutrisi untuk resep '{recipe.recipe_id}' ({recipe.nama_masakan}) "
                    "tidak lengkap (terdapat nilai null atau 0)."
                )

            recipe_usage_counts[recipe.recipe_id] += 1

            servings = float(item.servings)
            day_cal += float(recipe.kalori_kkal or 0.0) * servings
            day_carbs += float(recipe.karbohidrat_g or 0.0) * servings
            day_protein += float(recipe.protein_g or 0.0) * servings
            day_fat += float(recipe.lemak_g or 0.0) * servings

        day_cal_r = round(day_cal, 2)
        day_carbs_r = round(day_carbs, 2)
        day_protein_r = round(day_protein, 2)
        day_fat_r = round(day_fat, 2)

        total_cal += day_cal_r
        total_carbs += day_carbs_r
        total_protein += day_protein_r
        total_fat += day_fat_r

        cal_dev = _calc_deviation_pct(day_cal_r, target_nutrition.target_calories)
        carbs_dev = _calc_deviation_pct(day_carbs_r, target_nutrition.carbs_g)
        protein_dev = _calc_deviation_pct(day_protein_r, target_nutrition.protein_g)
        fat_dev = _calc_deviation_pct(day_fat_r, target_nutrition.fat_g)

        checks = (
            ("kalori", day_cal_r, target_nutrition.target_calories, cal_dev),
            ("karbohidrat", day_carbs_r, target_nutrition.carbs_g, carbs_dev),
            ("protein", day_protein_r, target_nutrition.protein_g, protein_dev),
            ("lemak", day_fat_r, target_nutrition.fat_g, fat_dev),
        )
        day_within_tol = True
        for label, actual_val, target_val, dev_pct in checks:
            if target_val > 0 and abs(dev_pct) > effective_tolerance:
                day_within_tol = False
                msg = (
                    f"Hari {day_plan.day}: total {label} ({actual_val}) menyimpang "
                    f"{dev_pct:+.2f}% dari target ({target_val}), di luar toleransi ±{effective_tolerance}%."
                )
                soft_violations.append(msg)
                warnings.append(msg)

        daily_summaries.append(
            DayNutritionSummary(
                day=day_plan.day,
                actual=NutritionTotals(
                    calories=day_cal_r,
                    carbs_g=day_carbs_r,
                    protein_g=day_protein_r,
                    fat_g=day_fat_r,
                ),
                calorie_deviation_pct=cal_dev,
                carbs_deviation_pct=carbs_dev,
                protein_deviation_pct=protein_dev,
                fat_deviation_pct=fat_dev,
                within_tolerance=day_within_tol,
            )
        )

    for recipe_id, count in recipe_usage_counts.items():
        if count > effective_max_repeats:
            recipe_name = recipes_by_id[recipe_id].nama_masakan
            msg = (
                f"Resep '{recipe_id}' ({recipe_name}) muncul {count} kali, "
                f"melebihi batas pengulangan maksimal {effective_max_repeats} kali."
            )
            soft_violations.append(msg)
            warnings.append(msg)

    overall_within_tolerance = all(summary.within_tolerance for summary in daily_summaries)

    if hard_violations:
        is_valid = False
        status: Literal["valid", "adjusted", "failed"] = "failed"
        rejection_reason = "; ".join(hard_violations)
    elif soft_violations:
        is_valid = True
        status = "adjusted"
        rejection_reason = None
    else:
        is_valid = True
        status = "valid"
        rejection_reason = None

    return ValidationResult(
        is_valid=is_valid,
        status=status,
        rejection_reason=rejection_reason,
        within_tolerance=overall_within_tolerance,
        hard_violations=hard_violations,
        soft_violations=soft_violations,
        warnings=warnings,
        daily_summaries=daily_summaries,
        total_actual_nutrition=NutritionTotals(
            calories=round(total_cal, 2),
            carbs_g=round(total_carbs, 2),
            protein_g=round(total_protein, 2),
            fat_g=round(total_fat, 2),
        ),
    )

