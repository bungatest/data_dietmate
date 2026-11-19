import pytest

from app.services.macro_service import calculate_macros, validate_macro_percentages


def test_macro_default_calculation():
    # Contoh dari guideline: 2000 kkal dengan 50% karbo, 20% protein, 30% lemak
    result = calculate_macros(target_calories=2000.0)
    assert result["carbs_g"] == 250.0
    assert result["protein_g"] == 100.0
    assert result["fat_g"] == 66.67
    assert result["carbs_pct"] == 50.0
    assert result["protein_pct"] == 20.0
    assert result["fat_pct"] == 30.0


def test_macro_custom_valid_percentages():
    result = calculate_macros(
        target_calories=1800.0,
        carbs_pct=55.0,
        protein_pct=20.0,
        fat_pct=25.0,
    )
    assert result["carbs_g"] == 247.5
    assert result["protein_g"] == 90.0
    assert result["fat_g"] == 50.0


def test_macro_percentage_sum_must_be_100():
    with pytest.raises(ValueError, match="100%"):
        validate_macro_percentages(carbs_pct=50.0, protein_pct=20.0, fat_pct=25.0)


@pytest.mark.parametrize(
    ("carbs", "protein", "fat"),
    [
        (40.0, 25.0, 35.0),  # carbs < 45% dan protein > 20%
        (70.0, 10.0, 20.0),  # carbs > 65%
        (60.0, 5.0, 35.0),   # protein < 10%
        (45.0, 15.0, 40.0),  # fat > 35%
    ],
)
def test_macro_out_of_range(carbs: float, protein: float, fat: float):
    with pytest.raises(ValueError):
        calculate_macros(target_calories=2000.0, carbs_pct=carbs, protein_pct=protein, fat_pct=fat)

