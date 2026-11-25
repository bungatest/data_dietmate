"""Test perbaikan integrasi FE↔BE: kode alergi/preferensi frontend, kategori slot, token & kepemilikan plan."""

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import Session

from app.core.security import create_access_token, decode_access_token
from app.db.database import _add_missing_columns
from app.models.recipe import Recipe
from app.services.mealplan_service import _split_ingredients, _split_instructions
from app.services.validation_service import RecipeData, find_matching_allergens

PROFILE = {
    "age": 25,
    "gender": "male",
    "weight_kg": 70.0,
    "height_cm": 175.0,
    "activity_level": "moderate",
    "pal": 1.55,
}


def _payload(**prefs):
    base = {"goal": "maintenance", "duration_days": 2, "allergies": [], "food_preferences": []}
    base.update(prefs)
    return {"profile": PROFILE, "preferences": base}


def _recipe_ids(plan: dict) -> list[str]:
    return [meal["recipe"]["id"] for day in plan["days"] for meal in day["meals"]]


def _register(client: TestClient, email: str) -> str:
    res = client.post(
        "/api/v1/auth/register",
        json={"name": "Tester", "email": email, "password": "rahasia123"},
    )
    assert res.status_code == 201
    return res.json()["access_token"]


# ---------- Alergi & preferensi dari kode frontend ----------

def test_frontend_allergy_codes_are_matched():
    recipe = RecipeData("X", "Sate Udang", 100, 1, 1, 1, "- udang - kacang tanah - susu - tepung terigu")
    matched = find_matching_allergens(
        recipe, ["nut_free", "shellfish_free", "dairy_free", "gluten_free"]
    )
    assert matched == ["kacang", "kerang/udang", "susu", "gluten"]


def test_shellfish_code_does_not_block_plain_fish():
    recipe = RecipeData("X", "Ikan Bakar", 100, 1, 1, 1, "- 200 gram ikan nila")
    assert find_matching_allergens(recipe, ["shellfish_free"]) == []


def test_generate_excludes_shellfish_with_frontend_code(client: TestClient):
    res = client.post("/api/v1/meal-plans/generate", json=_payload(allergies=["shellfish_free"]))
    assert res.status_code == 201
    assert "RCP_0003" not in _recipe_ids(res.json())


def test_generate_vegetarian_excludes_meat(client: TestClient):
    res = client.post("/api/v1/meal-plans/generate", json=_payload(food_preferences=["vegetarian"]))
    assert res.status_code == 201
    # Hanya Tumis Labu Siam (RCP_0002) yang tidak mengandung daging/ayam/udang
    assert set(_recipe_ids(res.json())) == {"RCP_0002"}


def test_main_meals_skip_drink_and_sauce_categories(client: TestClient, db_session: Session):
    db_session.add_all(
        [
            Recipe(recipe_id="RCP_9001", nama_masakan="Jus Jeruk", kategori="Minuman",
                   kalori_kkal=650.0, protein_g=2.0, karbohidrat_g=150.0, lemak_g=1.0, bahan_bahan="- jeruk"),
            Recipe(recipe_id="RCP_9002", nama_masakan="Sambal Matah", kategori="Saus dan Bumbu",
                   kalori_kkal=650.0, protein_g=2.0, karbohidrat_g=20.0, lemak_g=60.0, bahan_bahan="- cabai"),
        ]
    )
    db_session.commit()
    res = client.post("/api/v1/meal-plans/generate", json=_payload(duration_days=3))
    assert res.status_code == 201
    ids = _recipe_ids(res.json())
    assert "RCP_9001" not in ids
    assert "RCP_9002" not in ids


# ---------- Parsing bahan & langkah format dataset ----------

def test_split_dataset_ingredients_and_steps():
    assert _split_ingredients("- 1 sdm low-fat milk - 2 butir telur - 50 g bakso") == [
        "1 sdm low-fat milk",
        "2 butir telur",
        "50 g bakso",
    ]
    assert _split_instructions("1. Rebus air. 2. Masukkan 1.5 sdm gula. 3. Sajikan.") == [
        "Rebus air.",
        "Masukkan 1.5 sdm gula.",
        "Sajikan.",
    ]


# ---------- Token & kepemilikan plan ----------

def test_token_roundtrip_and_tamper_detection():
    token = create_access_token("USR_abc")
    assert decode_access_token(token) == "USR_abc"

    header, payload, signature = token.split(".")
    tampered = f"{header}.{payload}.{'A' * len(signature)}"
    try:
        decode_access_token(tampered)
    except ValueError:
        pass
    else:
        raise AssertionError("Token dengan tanda tangan salah harus ditolak")

    expired = create_access_token("USR_abc", expires_minutes=-1)
    try:
        decode_access_token(expired)
    except ValueError:
        pass
    else:
        raise AssertionError("Token kedaluwarsa harus ditolak")


def test_progress_and_plan_ownership_are_per_user(client: TestClient):
    token_a = _register(client, "a@example.com")
    _register(client, "b@example.com")

    res = client.post(
        "/api/v1/meal-plans/generate",
        json=_payload(),
        headers={"Authorization": f"Bearer {token_a}"},
    )
    assert res.status_code == 201
    plan_id = res.json()["plan_id"]

    login_a = client.post("/api/v1/auth/login", json={"email": "a@example.com", "password": "rahasia123"})
    login_b = client.post("/api/v1/auth/login", json={"email": "b@example.com", "password": "rahasia123"})
    assert login_a.json()["progress"]["has_meal_plan"] is True
    assert login_b.json()["progress"]["has_meal_plan"] is False

    token_b = login_b.json()["access_token"]
    own = client.get(f"/api/v1/meal-plans/{plan_id}", headers={"Authorization": f"Bearer {token_a}"})
    other = client.get(f"/api/v1/meal-plans/{plan_id}", headers={"Authorization": f"Bearer {token_b}"})
    anonymous = client.get(f"/api/v1/meal-plans/{plan_id}")
    assert own.status_code == 200
    assert own.json()["source"] == "stub"
    assert other.status_code == 404
    assert anonymous.status_code == 404

    me = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token_a}"})
    assert me.status_code == 200
    assert me.json()["user"]["email"] == "a@example.com"


def test_invalid_token_is_rejected(client: TestClient):
    res = client.post(
        "/api/v1/meal-plans/generate",
        json=_payload(),
        headers={"Authorization": "Bearer bukan.token.valid"},
    )
    assert res.status_code == 401
    assert client.get("/api/v1/auth/me").status_code == 401


# ---------- Migrasi kolom ringan ----------

def test_add_missing_columns_upgrades_old_meal_plans_table():
    engine = create_engine("sqlite://")
    with engine.begin() as conn:
        conn.execute(text("CREATE TABLE meal_plans (plan_id VARCHAR(50) PRIMARY KEY)"))
        conn.execute(text("INSERT INTO meal_plans (plan_id) VALUES ('MP_old')"))

    _add_missing_columns(engine)
    _add_missing_columns(engine)  # idempotent

    columns = {c["name"] for c in inspect(engine).get_columns("meal_plans")}
    assert {"user_id", "source"} <= columns
    with engine.connect() as conn:
        assert conn.execute(text("SELECT source FROM meal_plans")).scalar_one() == "stub"


# ---------- Hanya 3 waktu makan (tanpa snack) ----------

def test_meal_plan_has_exactly_three_meals_per_day(client: TestClient):
    payload = _payload(duration_days=3)
    payload["meals_per_day"] = 5  # field lama diabaikan
    res = client.post("/api/v1/meal-plans/generate", json=payload)
    assert res.status_code == 201
    for day in res.json()["days"]:
        assert [m["meal_type"] for m in day["meals"]] == ["breakfast", "lunch", "dinner"]


def test_snack_meal_type_is_rejected_by_validation_endpoint(client: TestClient):
    res = client.post(
        "/api/v1/nutrition/validate",
        json={
            "days": [{"day": 1, "meals": [
                {"recipe_id": "RCP_0001", "recipe_name": "Toge Telur", "servings": 1, "meal_type": "snack"}
            ]}],
            "target_nutrition": {"target_calories": 2000, "carbs_g": 250, "protein_g": 100, "fat_g": 67},
        },
    )
    assert res.status_code == 422
