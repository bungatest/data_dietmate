from fastapi.testclient import TestClient


def test_health_endpoint(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_auth_register_and_login_flow(client: TestClient):
    # 1. Register akun baru
    reg_payload = {
        "name": "Budi Santoso",
        "email": "budi@example.com",
        "password": "password123",
    }
    reg_res = client.post("/api/v1/auth/register", json=reg_payload)
    assert reg_res.status_code == 201
    user_data = reg_res.json()["user"]
    assert user_data["name"] == "Budi Santoso"
    assert user_data["email"] == "budi@example.com"
    assert user_data["id"].startswith("USR_")

    # 2. Login dengan akun yang baru dibuat
    login_payload = {
        "email": "budi@example.com",
        "password": "password123",
    }
    login_res = client.post("/api/v1/auth/login", json=login_payload)
    assert login_res.status_code == 200
    auth_data = login_res.json()
    assert auth_data["user"]["email"] == "budi@example.com"
    assert "progress" in auth_data

    # 3. Login gagal dengan password salah
    bad_login = client.post(
        "/api/v1/auth/login",
        json={"email": "budi@example.com", "password": "wrongpassword"},
    )
    assert bad_login.status_code == 401


def test_generate_meal_plan_unified_endpoint(client: TestClient):
    """Menguji pembuatan meal plan menggunakan payload standar PRD / Frontend Next.js."""
    payload = {
        "profile": {
            "age": 25,
            "gender": "male",
            "weight_kg": 70.0,
            "height_cm": 175.0,
            "activity_level": "moderate",
            "pal": 1.55,
        },
        "preferences": {
            "goal": "weight_loss",
            "duration_days": 2,
            "allergies": ["udang"],
            "food_preferences": ["ayam"],
        },
    }
    res = client.post("/api/v1/meal-plans/generate", json=payload)
    assert res.status_code == 201
    data = res.json()

    # Validasi struktur root
    assert data["plan_id"].startswith("MP_")
    assert data["source"] == "stub"
    assert "nutrition_summary" in data
    assert data["nutrition_summary"]["bmi"] == 22.86
    assert len(data["days"]) == 2
    assert data["validation"]["passed"] is True

    # Validasi detail resep pada hari pertama
    first_meal = data["days"][0]["meals"][0]
    assert "recipe" in first_meal
    assert "id" in first_meal["recipe"]
    assert "name" in first_meal["recipe"]
    assert len(first_meal["recipe"]["ingredients"]) > 0
    assert len(first_meal["recipe"]["instructions"]) > 0

    # Pastikan resep yang mengandung alergen (udang) tidak ada
    all_recipe_ids = [
        meal["recipe"]["id"]
        for day in data["days"]
        for meal in day["meals"]
    ]
    assert "RCP_0003" not in all_recipe_ids

    # Uji ambil data kembali via GET /api/v1/meal-plans/{id}
    get_res = client.get(f"/api/v1/meal-plans/{data['plan_id']}")
    assert get_res.status_code == 200
    fetched = get_res.json()
    assert fetched["plan_id"] == data["plan_id"]