from fastapi.testclient import TestClient


def test_health_endpoint(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_calculate_nutrition_endpoint(client: TestClient):
    payload = {
        "age": 25,
        "gender": "male",
        "weight_kg": 70.0,
        "height_cm": 175.0,
        "activity_level": "moderate",
        "diet_goal": "maintain",
        "allergies": ["udang"],
        "preferences": ["ayam"],
    }
    response = client.post("/nutrition/calculate", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["bmi"] == 22.86
    assert data["bmi_category"] == "Normal"
    assert data["bmi_standard"] == "kemenkes"
    assert data["bmr"] == 1673.75
    assert data["tdee"] == 2594.31
    assert data["target_calories"] == 2594.31
    assert data["macros"]["carbs_pct"] == 50.0
    assert data["macros"]["protein_pct"] == 20.0
    assert data["macros"]["fat_pct"] == 30.0
    assert data["warnings"] == []


def test_calculate_nutrition_low_calorie_warning(client: TestClient):
    payload = {
        "age": 60,
        "gender": "female",
        "weight_kg": 40.0,
        "height_cm": 150.0,
        "activity_level": "sedentary",
        "diet_goal": "lose_weight",
        "allergies": [],
        "preferences": [],
    }
    response = client.post("/nutrition/calculate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["target_calories"] < 1200.0
    assert len(data["warnings"]) == 1
    assert "1200" in data["warnings"][0]


def test_validate_nutrition_endpoint_rejects_allergen_from_db(client: TestClient):
    payload = {
        "target_nutrition": {
            "target_calories": 1500.0,
            "carbs_g": 187.5,
            "protein_g": 75.0,
            "fat_g": 50.0,
        },
        "allergies": ["udang"],
        "days": [
            {
                "day": 1,
                "meals": [
                    {
                        "recipe_id": "RCP_0003",
                        "recipe_name": "Dimsum Ayam Udang",
                        "servings": 3.0,
                        "meal_type": "lunch",
                    }
                ],
            }
        ],
    }
    response = client.post("/nutrition/validate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["is_valid"] is False
    assert data["status"] == "failed"
    assert "allergen" in data["rejection_reason"].lower()


def test_generate_and_get_mealplan_persisted(client: TestClient):
    payload = {
        "user_profile": {
            "age": 25,
            "gender": "male",
            "weight_kg": 70.0,
            "height_cm": 175.0,
            "activity_level": "moderate",
            "diet_goal": "maintain",
            "allergies": ["udang"],
            "preferences": ["ayam"],
        },
        "duration_days": 2,
        "meals_per_day": 3,
    }
    create_res = client.post("/mealplan/generate", json=payload)
    assert create_res.status_code == 201
    created = create_res.json()

    assert created["plan_id"].startswith("MP_")
    assert len(created["days"]) == 2
    assert created["validation_status"] in ("valid", "adjusted")

    # Pastikan tidak ada resep mengandung udang (RCP_0003) yang lolos
    all_recipe_ids = [
        meal["recipe_id"]
        for day in created["days"]
        for meal in day["meals"]
    ]
    assert "RCP_0003" not in all_recipe_ids

    # Pastikan bisa diambil kembali dari DB melalui GET /mealplan/{id}
    get_res = client.get(f"/mealplan/{created['plan_id']}")
    assert get_res.status_code == 200
    fetched = get_res.json()
    assert fetched["plan_id"] == created["plan_id"]
    assert fetched["days"] == created["days"]


def test_get_mealplan_not_found(client: TestClient):
    response = client.get("/mealplan/MP_DOES_NOT_EXIST")
    assert response.status_code == 404

