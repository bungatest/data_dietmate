from typing import Final

PAL_FACTORS: Final[dict[str, float]] = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "active": 1.725,
    "very_active": 1.9,
}

GOAL_ADJUSTMENTS: Final[dict[str, float]] = {
    "lose_weight": -500.0,
    "maintain": 0.0,
    "gain_muscle": 300.0,
}

GENDER_OFFSETS: Final[dict[str, float]] = {
    "male": 5.0,
    "female": -161.0,
}

MIN_SAFE_ADULT_CALORIES: Final[float] = 1200.0


def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: str) -> float:
    """Menghitung Basal Metabolic Rate (BMR) menggunakan rumus Mifflin-St Jeor."""
    if weight_kg <= 0 or height_cm <= 0 or age <= 0:
        raise ValueError("weight_kg, height_cm, dan age harus lebih besar dari 0.")

    normalized_gender = gender.lower()
    if normalized_gender not in GENDER_OFFSETS:
        raise ValueError("gender harus 'male' atau 'female'.")

    return (10.0 * weight_kg) + (6.25 * height_cm) - (5.0 * age) + GENDER_OFFSETS[normalized_gender]


def calculate_tdee(bmr: float, activity_level: str) -> float:
    """Menghitung Total Daily Energy Expenditure (TDEE) dari BMR dan faktor aktivitas PAL."""
    if bmr <= 0:
        raise ValueError("bmr harus lebih besar dari 0.")

    normalized_level = activity_level.lower()
    if normalized_level not in PAL_FACTORS:
        supported = ", ".join(PAL_FACTORS.keys())
        raise ValueError(f"activity_level tidak valid. Pilihan: {supported}.")

    return bmr * PAL_FACTORS[normalized_level]


def calculate_target_calories(tdee: float, diet_goal: str) -> float:
    """Menghitung target kalori harian berdasarkan tujuan diet tanpa memblokir nilai < 1200."""
    if tdee <= 0:
        raise ValueError("tdee harus lebih besar dari 0.")

    normalized_goal = diet_goal.lower()
    if normalized_goal not in GOAL_ADJUSTMENTS:
        supported = ", ".join(GOAL_ADJUSTMENTS.keys())
        raise ValueError(f"diet_goal tidak valid. Pilihan: {supported}.")

    return tdee + GOAL_ADJUSTMENTS[normalized_goal]


def get_calorie_warnings(target_calories: float) -> list[str]:
    """Mengembalikan peringatan jika target kalori harian berada di bawah batas aman dewasa."""
    if target_calories < MIN_SAFE_ADULT_CALORIES:
        return [
            (
                f"Target kalori harian ({target_calories:.2f} kkal) di bawah "
                f"{int(MIN_SAFE_ADULT_CALORIES)} kkal untuk orang dewasa. "
                "Hasil tetap ditampilkan, namun disarankan berkonsultasi dengan tenaga gizi."
            )
        ]
    return []

