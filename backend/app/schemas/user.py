from typing import Annotated, Literal

from pydantic import AfterValidator, BaseModel, ConfigDict, Field, model_validator

# Berat badan selalu dicatat dengan 2 angka di belakang koma (mis. 58.75 kg).
WeightKg = Annotated[
    float,
    Field(ge=30.0, le=300.0, description="Berat badan dalam kilogram (30–300, 2 desimal)"),
    AfterValidator(lambda value: round(value, 2)),
]

# Tinggi badan selalu dicatat dengan 1 angka di belakang koma (mis. 165.5 cm).
HeightCm = Annotated[
    float,
    Field(ge=100.0, le=250.0, description="Tinggi badan dalam sentimeter (100–250, 1 desimal)"),
    AfterValidator(lambda value: round(value, 1)),
]


class MacroDistribution(BaseModel):
    """Konfigurasi persentase distribusi energi makronutrien (total harus 100%)."""

    carbs_pct: float = Field(default=50.0, ge=45.0, le=65.0, description="Persentase karbohidrat (45–65%)")
    protein_pct: float = Field(default=20.0, ge=10.0, le=20.0, description="Persentase protein (10–20%)")
    fat_pct: float = Field(default=30.0, ge=20.0, le=35.0, description="Persentase lemak (20–35%)")

    @model_validator(mode="after")
    def check_sum_is_100(self) -> "MacroDistribution":
        total = self.carbs_pct + self.protein_pct + self.fat_pct
        if abs(total - 100.0) > 1e-6:
            raise ValueError(f"Total persentase makronutrien harus tepat 100% (saat ini: {total}%).")
        return self


class UserProfile(BaseModel):
    """Profil antropometri, aktivitas, tujuan diet, dan pantangan pengguna."""

    age: int = Field(..., ge=18, le=100, description="Usia pengguna dalam tahun (18–100)")
    gender: Literal["male", "female"] = Field(..., description="Jenis kelamin: 'male' atau 'female'")
    weight_kg: WeightKg
    height_cm: HeightCm
    activity_level: Literal["sedentary", "light", "moderate", "active", "very_active"] = Field(
        ...,
        description="Tingkat aktivitas fisik harian (PAL)",
    )
    diet_goal: Literal["lose_weight", "maintain", "gain_muscle"] = Field(
        ...,
        description="Tujuan diet pengguna",
    )
    allergies: list[str] = Field(default_factory=list, description="Daftar bahan alergen/pantangan")
    preferences: list[str] = Field(default_factory=list, description="Daftar preferensi makanan")
    macro_distribution: MacroDistribution | None = Field(
        default=None,
        description="Opsional: kustomisasi rasio persentase makronutrien (default 50% karbo, 20% protein, 30% lemak)",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "age": 25,
                "gender": "male",
                "weight_kg": 70.0,
                "height_cm": 175.0,
                "activity_level": "moderate",
                "diet_goal": "maintain",
                "allergies": ["udang", "kacang"],
                "preferences": ["ayam", "sayuran"],
            }
        }
    )

