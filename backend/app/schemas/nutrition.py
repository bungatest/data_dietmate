from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


# Meal plan DietMate hanya memiliki 3 waktu makan per hari.
MealType = Literal["breakfast", "lunch", "dinner"]


class MacroTargets(BaseModel):
    """Target kebutuhan makronutrien harian dalam gram beserta persentase energinya."""

    carbs_g: float
    protein_g: float
    fat_g: float
    carbs_pct: float
    protein_pct: float
    fat_pct: float


class NutritionResult(BaseModel):
    """Hasil perhitungan kebutuhan nutrisi pengguna (BMI, BMR, TDEE, kalori, dan makro)."""

    bmi: float
    bmi_category: str
    bmi_standard: str
    bmr: float
    tdee: float
    target_calories: float
    macros: MacroTargets
    warnings: list[str] = Field(default_factory=list)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "bmi": 22.86,
                "bmi_category": "Normal",
                "bmi_standard": "kemenkes",
                "bmr": 1673.75,
                "tdee": 2594.31,
                "target_calories": 2594.31,
                "macros": {
                    "carbs_g": 324.29,
                    "protein_g": 129.72,
                    "fat_g": 86.48,
                    "carbs_pct": 50.0,
                    "protein_pct": 20.0,
                    "fat_pct": 30.0,
                },
                "warnings": [],
            }
        }
    )


class NutritionTotals(BaseModel):
    """Total nilai nutrisi aktual yang dihitung ulang dari database resep."""

    calories: float
    carbs_g: float
    protein_g: float
    fat_g: float


class TargetNutritionInput(BaseModel):
    """Target nutrisi harian yang menjadi acuan validasi meal plan."""

    target_calories: float = Field(..., gt=0, description="Target kalori harian (kkal)")
    carbs_g: float = Field(..., ge=0, description="Target karbohidrat harian (gram)")
    protein_g: float = Field(..., ge=0, description="Target protein harian (gram)")
    fat_g: float = Field(..., ge=0, description="Target lemak harian (gram)")


class MealValidationItem(BaseModel):
    """Item resep dalam meal plan yang akan divalidasi oleh backend."""

    recipe_id: str = Field(..., min_length=1)
    recipe_name: str | None = None
    servings: float = Field(..., description="Jumlah porsi; divalidasi > 0 dan <= 10 di service")
    meal_type: MealType = "lunch"


class DayValidationInput(BaseModel):
    """Susunan menu satu hari yang akan diperiksa nutrisinya."""

    day: int = Field(default=1, ge=1)
    meals: list[MealValidationItem] = Field(..., min_length=1)


class MealPlanValidationRequest(BaseModel):
    """Request payload untuk endpoint POST /nutrition/validate."""

    target_nutrition: TargetNutritionInput
    allergies: list[str] = Field(default_factory=list)
    days: list[DayValidationInput] | None = None
    meals: list[MealValidationItem] | None = None
    tolerance_pct: float | None = Field(default=None, gt=0, le=100)
    max_recipe_repeats: int | None = Field(default=None, ge=1)

    @model_validator(mode="after")
    def normalize_days_or_meals(self) -> "MealPlanValidationRequest":
        if not self.days and not self.meals:
            raise ValueError("Harus menyertakan minimal salah satu dari 'days' atau 'meals'.")
        if not self.days and self.meals:
            self.days = [DayValidationInput(day=1, meals=self.meals)]
        return self

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "target_nutrition": {
                    "target_calories": 2000.0,
                    "carbs_g": 250.0,
                    "protein_g": 100.0,
                    "fat_g": 66.67,
                },
                "allergies": ["udang"],
                "days": [
                    {
                        "day": 1,
                        "meals": [
                            {
                                "recipe_id": "RCP_0001",
                                "recipe_name": "Toge Telur",
                                "servings": 2.0,
                                "meal_type": "breakfast",
                            }
                        ],
                    }
                ],
            }
        }
    )


class DayNutritionSummary(BaseModel):
    """Ringkasan hasil perhitungan ulang nutrisi dan deviasi terhadap target per hari."""

    day: int
    actual: NutritionTotals
    calorie_deviation_pct: float
    carbs_deviation_pct: float
    protein_deviation_pct: float
    fat_deviation_pct: float
    within_tolerance: bool


class ValidationResult(BaseModel):
    """Hasil validasi meal plan terhadap hard constraint dan soft constraint."""

    is_valid: bool
    status: Literal["valid", "adjusted", "failed"]
    rejection_reason: str | None = None
    within_tolerance: bool
    hard_violations: list[str] = Field(default_factory=list)
    soft_violations: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    daily_summaries: list[DayNutritionSummary] = Field(default_factory=list)
    total_actual_nutrition: NutritionTotals

