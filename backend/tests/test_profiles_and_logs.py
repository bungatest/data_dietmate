"""Test tabel user_profiles, generation_logs, dan endpoint meal plan terbaru."""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.generation_log import GenerationLog
from app.models.user_profile import UserProfileRecord

PROFILE = {
    "age": 30,
    "gender": "female",
    "weight_kg": 60.0,
    "height_cm": 160.0,
    "activity_level": "light",
    "pal": 1.375,
}
PREFERENCES = {
    "goal": "weight_loss",
    "duration_days": 2,
    "allergies": ["shellfish_free"],
    "food_preferences": ["high_protein"],
}


def _auth(client: TestClient, email: str = "sari@example.com") -> dict[str, str]:
    res = client.post(
        "/api/v1/auth/register",
        json={"name": "Sari", "email": email, "password": "rahasia123"},
    )
    assert res.status_code == 201
    return {"Authorization": f"Bearer {res.json()['access_token']}"}


def _login_progress(client: TestClient, email: str = "sari@example.com") -> dict:
    res = client.post("/api/v1/auth/login", json={"email": email, "password": "rahasia123"})
    assert res.status_code == 200
    return res.json()["progress"]


# ---------- user_profiles ----------

def test_profile_endpoints_require_login(client: TestClient):
    assert client.get("/api/v1/users/me/profile").status_code == 401
    assert client.put("/api/v1/users/me/profile", json=PROFILE).status_code == 401


def test_profile_and_preferences_roundtrip_and_progress(client: TestClient):
    headers = _auth(client)

    empty = client.get("/api/v1/users/me/profile", headers=headers)
    assert empty.status_code == 200
    assert empty.json() == {"profile": None, "preferences": None, "updated_at": None}
    assert _login_progress(client) == {
        "profile_completed": False,
        "preferences_completed": False,
        "has_meal_plan": False,
    }

    # Preferensi sebelum profil ditolak
    early = client.put("/api/v1/users/me/preferences", json=PREFERENCES, headers=headers)
    assert early.status_code == 409

    saved = client.put("/api/v1/users/me/profile", json=PROFILE, headers=headers)
    assert saved.status_code == 200
    assert saved.json()["profile"] == PROFILE
    assert saved.json()["preferences"] is None
    assert _login_progress(client)["profile_completed"] is True
    assert _login_progress(client)["preferences_completed"] is False

    prefs = client.put("/api/v1/users/me/preferences", json=PREFERENCES, headers=headers)
    assert prefs.status_code == 200
    assert prefs.json()["preferences"] == PREFERENCES
    assert _login_progress(client)["preferences_completed"] is True

    # Update profil tidak menghapus preferensi
    updated = client.put("/api/v1/users/me/profile", json={**PROFILE, "weight_kg": 58.5}, headers=headers)
    assert updated.json()["profile"]["weight_kg"] == 58.5
    assert updated.json()["preferences"] == PREFERENCES


def test_profiles_are_isolated_between_users(client: TestClient):
    headers_a = _auth(client, "a@example.com")
    headers_b = _auth(client, "b@example.com")
    client.put("/api/v1/users/me/profile", json=PROFILE, headers=headers_a)

    other = client.get("/api/v1/users/me/profile", headers=headers_b)
    assert other.json()["profile"] is None


def test_generate_saves_latest_profile_and_legacy_goal_is_normalized(
    client: TestClient, db_session: Session
):
    headers = _auth(client)
    payload = {"profile": PROFILE, "preferences": {**PREFERENCES, "goal": "lose_weight"}}
    res = client.post("/api/v1/meal-plans/generate", json=payload, headers=headers)
    assert res.status_code == 201

    stored = client.get("/api/v1/users/me/profile", headers=headers).json()
    assert stored["profile"] == PROFILE
    assert stored["preferences"]["goal"] == "weight_loss"
    assert db_session.query(UserProfileRecord).count() == 1


# ---------- meal plan terbaru ----------

def test_latest_meal_plan_per_user(client: TestClient):
    headers = _auth(client)
    assert client.get("/api/v1/meal-plans/latest", headers=headers).status_code == 404
    assert client.get("/api/v1/meal-plans/latest").status_code == 401

    payload = {"profile": PROFILE, "preferences": PREFERENCES}
    client.post("/api/v1/meal-plans/generate", json=payload, headers=headers)
    second = client.post("/api/v1/meal-plans/generate", json=payload, headers=headers).json()

    latest = client.get("/api/v1/meal-plans/latest", headers=headers)
    assert latest.status_code == 200
    assert latest.json()["plan_id"] == second["plan_id"]

    other = _auth(client, "lain@example.com")
    assert client.get("/api/v1/meal-plans/latest", headers=other).status_code == 404


# ---------- generation_logs ----------

def test_successful_generation_is_logged(client: TestClient, db_session: Session):
    headers = _auth(client)
    res = client.post(
        "/api/v1/meal-plans/generate",
        json={"profile": PROFILE, "preferences": PREFERENCES},
        headers=headers,
    )
    plan = res.json()

    logs = db_session.query(GenerationLog).all()
    assert len(logs) == 1
    log = logs[0]
    assert log.status == "success"
    assert log.source == "stub"
    assert log.plan_id == plan["plan_id"]
    assert log.user_id is not None
    assert log.request_payload["preferences"]["allergies"] == ["shellfish_free"]
    assert log.selected_recipe_ids == [m["recipe"]["id"] for d in plan["days"] for m in d["meals"]]
    assert log.validation_passed == plan["validation"]["passed"]
    assert log.validation_warnings == plan["validation"]["warnings"]
    assert log.latency_ms >= 0
    # Kolom RAG kosong untuk generator stub
    assert log.retrieval_query is None and log.prompt is None and log.llm_raw_output is None


def test_failed_generation_is_logged(client: TestClient, db_session: Session):
    # Vegetarian + alergi semua bahan yang tersisa -> tidak ada resep aman -> 404
    payload = {
        "profile": PROFILE,
        "preferences": {**PREFERENCES, "food_preferences": ["vegetarian"], "allergies": ["labu"]},
    }
    res = client.post("/api/v1/meal-plans/generate", json=payload)
    assert res.status_code == 404

    log = db_session.query(GenerationLog).one()
    assert log.status == "failed"
    assert log.plan_id is None
    assert log.user_id is None
    assert "LookupError" in (log.error_message or "")


def test_weight_is_stored_with_two_decimals(client: TestClient):
    headers = _auth(client)
    res = client.put(
        "/api/v1/users/me/profile",
        json={**PROFILE, "weight_kg": 58.756},
        headers=headers,
    )
    assert res.status_code == 200
    assert res.json()["profile"]["weight_kg"] == 58.76

    stored = client.get("/api/v1/users/me/profile", headers=headers).json()
    assert stored["profile"]["weight_kg"] == 58.76

    plan = client.post(
        "/api/v1/meal-plans/generate",
        json={"profile": {**PROFILE, "weight_kg": 58.75}, "preferences": PREFERENCES},
        headers=headers,
    )
    assert plan.status_code == 201
    # BMI dihitung dari berat desimal: 58.75 / 1.6^2 = 22.95
    assert plan.json()["nutrition_summary"]["bmi"] == 22.95


def test_height_is_stored_with_one_decimal(client: TestClient):
    headers = _auth(client)
    res = client.put(
        "/api/v1/users/me/profile",
        json={**PROFILE, "height_cm": 165.46},
        headers=headers,
    )
    assert res.status_code == 200
    assert res.json()["profile"]["height_cm"] == 165.5
    assert client.get("/api/v1/users/me/profile", headers=headers).json()["profile"]["height_cm"] == 165.5
