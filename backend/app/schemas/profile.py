from datetime import datetime

from pydantic import BaseModel

from app.schemas.mealplan import FrontendPreferences, FrontendUserProfile


class StoredProfileResponse(BaseModel):
    """Profil & preferensi tersimpan milik user aktif. Bernilai null jika belum diisi."""

    profile: FrontendUserProfile | None = None
    preferences: FrontendPreferences | None = None
    updated_at: datetime | None = None
