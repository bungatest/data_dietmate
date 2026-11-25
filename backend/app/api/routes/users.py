from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.mealplan import FrontendPreferences, FrontendUserProfile
from app.schemas.profile import StoredProfileResponse
from app.services.profile_service import (
    ProfileRequiredError,
    get_profile_record,
    to_response,
    update_preferences,
    upsert_profile,
)

router = APIRouter(prefix="/users/me", tags=["User Profile"])


@router.get(
    "/profile",
    response_model=StoredProfileResponse,
    summary="Ambil profil & preferensi tersimpan milik user aktif",
)
def get_my_profile(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return to_response(get_profile_record(db, user.id))


@router.put(
    "/profile",
    response_model=StoredProfileResponse,
    summary="Simpan / perbarui profil (usia, gender, tinggi, berat, aktivitas)",
)
def put_my_profile(
    profile: FrontendUserProfile,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return to_response(upsert_profile(db, user.id, profile))


@router.put(
    "/preferences",
    response_model=StoredProfileResponse,
    summary="Simpan / perbarui preferensi diet (tujuan, durasi, alergi, preferensi makanan)",
)
def put_my_preferences(
    preferences: FrontendPreferences,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return to_response(update_preferences(db, user.id, preferences))
    except ProfileRequiredError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
