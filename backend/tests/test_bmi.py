import pytest

from app.services.bmi_service import calculate_bmi, get_bmi_category


def test_bmi_normal():
    # BB=60kg, TB=165cm -> BMI ≈ 22.04
    result = calculate_bmi(weight_kg=60, height_cm=165)
    assert round(result, 2) == 22.04
    assert get_bmi_category(result, standard="kemenkes") == "Normal"


def test_bmi_kemenkes_categories():
    assert get_bmi_category(16.9, standard="kemenkes") == "Sangat Kurus"
    assert get_bmi_category(17.0, standard="kemenkes") == "Kurus"
    assert get_bmi_category(18.4, standard="kemenkes") == "Kurus"
    assert get_bmi_category(18.5, standard="kemenkes") == "Normal"
    assert get_bmi_category(25.0, standard="kemenkes") == "Normal"
    assert get_bmi_category(25.1, standard="kemenkes") == "Gemuk"
    assert get_bmi_category(27.0, standard="kemenkes") == "Gemuk"
    assert get_bmi_category(27.1, standard="kemenkes") == "Obesitas"


def test_bmi_who_categories():
    assert get_bmi_category(18.4, standard="who") == "Underweight"
    assert get_bmi_category(22.0, standard="who") == "Normal"
    assert get_bmi_category(26.5, standard="who") == "Overweight"
    assert get_bmi_category(30.0, standard="who") == "Obese"


def test_bmi_edge_cases():
    very_short = calculate_bmi(weight_kg=35, height_cm=100)
    assert very_short == 35.0
    very_tall = calculate_bmi(weight_kg=80, height_cm=220)
    assert round(very_tall, 2) == 16.53

    with pytest.raises(ValueError):
        calculate_bmi(weight_kg=0, height_cm=165)
    with pytest.raises(ValueError):
        calculate_bmi(weight_kg=60, height_cm=-170)
    with pytest.raises(ValueError):
        get_bmi_category(22.0, standard="invalid_standard")

