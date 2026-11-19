from typing import Final

DEFAULT_CARBS_PCT: Final[float] = 50.0
DEFAULT_PROTEIN_PCT: Final[float] = 20.0
DEFAULT_FAT_PCT: Final[float] = 30.0

MACRO_PERCENTAGE_RANGES: Final[dict[str, tuple[float, float]]] = {
    "carbs_pct": (45.0, 65.0),
    "protein_pct": (10.0, 20.0),
    "fat_pct": (20.0, 35.0),
}

KCAL_PER_GRAM: Final[dict[str, float]] = {
    "carbs": 4.0,
    "protein": 4.0,
    "fat": 9.0,
}


def validate_macro_percentages(
    carbs_pct: float,
    protein_pct: float,
    fat_pct: float,
) -> None:
    """Memvalidasi rentang distribusi energi makronutrien dan memastikan totalnya tepat 100%."""
    values = {
        "carbs_pct": carbs_pct,
        "protein_pct": protein_pct,
        "fat_pct": fat_pct,
    }
    for name, value in values.items():
        min_pct, max_pct = MACRO_PERCENTAGE_RANGES[name]
        if not (min_pct <= value <= max_pct):
            raise ValueError(f"{name} ({value}%) harus berada dalam rentang {min_pct}%–{max_pct}%.")

    total_pct = carbs_pct + protein_pct + fat_pct
    if abs(total_pct - 100.0) > 1e-6:
        raise ValueError(f"Total persentase makronutrien harus tepat 100% (saat ini: {total_pct}%).")


def calculate_macros(
    target_calories: float,
    carbs_pct: float = DEFAULT_CARBS_PCT,
    protein_pct: float = DEFAULT_PROTEIN_PCT,
    fat_pct: float = DEFAULT_FAT_PCT,
) -> dict[str, float]:
    """Mengonversi target kalori dan rasio persentase menjadi target gram karbohidrat, protein, dan lemak."""
    if target_calories <= 0:
        raise ValueError("target_calories harus lebih besar dari 0.")

    validate_macro_percentages(carbs_pct=carbs_pct, protein_pct=protein_pct, fat_pct=fat_pct)

    carbs_g = round((target_calories * (carbs_pct / 100.0)) / KCAL_PER_GRAM["carbs"], 2)
    protein_g = round((target_calories * (protein_pct / 100.0)) / KCAL_PER_GRAM["protein"], 2)
    fat_g = round((target_calories * (fat_pct / 100.0)) / KCAL_PER_GRAM["fat"], 2)

    return {
        "carbs_g": carbs_g,
        "protein_g": protein_g,
        "fat_g": fat_g,
        "carbs_pct": float(carbs_pct),
        "protein_pct": float(protein_pct),
        "fat_pct": float(fat_pct),
    }

