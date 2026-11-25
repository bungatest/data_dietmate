from sqlalchemy.orm import Session

from app.models.user_profile import UserProfileRecord
from app.schemas.mealplan import FrontendPreferences, FrontendUserProfile
from app.schemas.profile import StoredProfileResponse

# Nilai goal disimpan dalam format frontend agar bisa langsung dimuat ulang ke form.
_GOAL_TO_FRONTEND = {
    "lose_weight": "weight_loss",
    "maintain": "maintenance",
    "gain_muscle": "muscle_gain",
}


class ProfileRequiredError(Exception):
    """Preferensi tidak bisa disimpan sebelum profil diisi."""


def get_profile_record(db: Session, user_id: str) -> UserProfileRecord | None:
    return db.get(UserProfileRecord, user_id)


def to_response(record: UserProfileRecord | None) -> StoredProfileResponse:
    if record is None:
        return StoredProfileResponse()

    profile = FrontendUserProfile(
        age=record.age,
        gender=record.gender,  # type: ignore[arg-type]
        height_cm=record.height_cm,
        weight_kg=record.weight_kg,
        activity_level=record.activity_level,  # type: ignore[arg-type]
        pal=record.pal,
    )
    preferences = None
    if record.goal is not None:
        preferences = FrontendPreferences(
            goal=record.goal,  # type: ignore[arg-type]
            duration_days=record.duration_days or 7,
            allergies=list(record.allergies or []),
            food_preferences=list(record.food_preferences or []),
        )
    return StoredProfileResponse(profile=profile, preferences=preferences, updated_at=record.updated_at)


def _apply_profile(record: UserProfileRecord, profile: FrontendUserProfile) -> None:
    record.age = profile.age
    record.gender = profile.gender
    record.height_cm = profile.height_cm
    record.weight_kg = profile.weight_kg
    record.activity_level = profile.activity_level
    record.pal = profile.pal


def _apply_preferences(record: UserProfileRecord, preferences: FrontendPreferences) -> None:
    record.goal = _GOAL_TO_FRONTEND.get(preferences.goal, preferences.goal)
    record.duration_days = preferences.duration_days
    record.allergies = list(preferences.allergies)
    record.food_preferences = list(preferences.food_preferences)


def upsert_profile(
    db: Session,
    user_id: str,
    profile: FrontendUserProfile,
    preferences: FrontendPreferences | None = None,
    commit: bool = True,
) -> UserProfileRecord:
    """Membuat atau memperbarui profil (dan opsional preferensi) user."""
    record = get_profile_record(db, user_id)
    if record is None:
        record = UserProfileRecord(user_id=user_id, allergies=[], food_preferences=[])
        db.add(record)
    _apply_profile(record, profile)
    if preferences is not None:
        _apply_preferences(record, preferences)
    if commit:
        db.commit()
        db.refresh(record)
    return record


def update_preferences(db: Session, user_id: str, preferences: FrontendPreferences) -> UserProfileRecord:
    record = get_profile_record(db, user_id)
    if record is None:
        raise ProfileRequiredError("Lengkapi profil terlebih dahulu sebelum menyimpan preferensi.")
    _apply_preferences(record, preferences)
    db.commit()
    db.refresh(record)
    return record
