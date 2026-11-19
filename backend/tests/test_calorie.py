import pytest

from app.services.calorie_service import (
    calculate_bmr,
    calculate_target_calories,
    calculate_tdee,
    get_calorie_warnings,
)


def test_bmr_male():
    # Pria, 25 tahun, 70kg, 175cm
    # BMR = 10(70) + 6.25(175) - 5(25) + 5 = 1673.75
    result = calculate_bmr(weight_kg=70, height_cm=175, age=25, gender="male")
    assert result == 1673.75


def test_bmr_female():
    # Wanita, 25 tahun, 55kg, 160cm
    # BMR = 10(55) + 6.25(160) - 5(25) - 161 = 550 + 1000 - 125 - 161 = 1264.0
    result = calculate_bmr(weight_kg=55, height_cm=160, age=25, gender="female")
    assert result == 1264.0


@pytest.mark.parametrize(
    ("activity_level", "expected_multiplier"),
    [
        ("sedentary", 1.2),
        ("light", 1.375),
        ("moderate", 1.55),
        ("active", 1.725),
        ("very_active", 1.9),
    ],
)
def test_tdee_pal_levels(activity_level: str, expected_multiplier: float):
    bmr = 1500.0
    assert calculate_tdee(bmr, activity_level) == pytest.approx(bmr * expected_multiplier)


def test_target_calories_per_goal():
    tdee = 2200.0
    assert calculate_target_calories(tdee, "lose_weight") == 1700.0
    assert calculate_target_calories(tdee, "maintain") == 2200.0
    assert calculate_target_calories(tdee, "gain_muscle") == 2500.0


def test_low_calorie_warning_not_blocking():
    target = calculate_target_calories(1500.0, "lose_weight")
    assert target == 1000.0
    warnings = get_calorie_warnings(target)
    assert len(warnings) == 1
    assert "1200" in warnings[0]
    assert get_calorie_warnings(1200.0) == []


def test_calorie_invalid_inputs():
    with pytest.raises(ValueError):
        calculate_bmr(weight_kg=70, height_cm=175, age=25, gender="other")
    with pytest.raises(ValueError):
        calculate_tdee(bmr=1500.0, activity_level="unknown")
    with pytest.raises(ValueError):
        calculate_target_calories(tdee=2000.0, diet_goal="bulk_extreme")

