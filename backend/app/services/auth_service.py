import hashlib
import hmac
import secrets
from uuid import uuid4

from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.models.meal_plan import MealPlan
from app.models.user import User
from app.models.user_profile import UserProfileRecord
from app.schemas.auth import (
    AccountProgress,
    AuthResult,
    DietMateUser,
    LoginPayload,
    RegisterPayload,
)


def hash_password(password: str, salt: str | None = None) -> str:
    """Enkripsi Password Pengguna"""
    if not salt:
        salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        iterations=100000,
    )
    return f"{salt}${key.hex()}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verivikasi Password Pengguna"""
    try:
        salt, _ = hashed_password.split("$", 1)
        return hmac.compare_digest(hash_password(plain_password, salt), hashed_password)
    except ValueError:
        return False


def get_user_account_progress(db: Session, user_id: str) -> AccountProgress:
    """Status onboarding user berdasarkan tabel user_profiles dan meal_plans."""
    profile = db.get(UserProfileRecord, user_id)
    has_plan = db.query(MealPlan.plan_id).filter(MealPlan.user_id == user_id).first() is not None
    return AccountProgress(
        profile_completed=profile is not None,
        preferences_completed=profile is not None and profile.goal is not None,
        has_meal_plan=has_plan,
    )


def register_user(db: Session, payload: RegisterPayload) -> DietMateUser:
    """Mendaftarkan akun user baru ke database"""
    normalized_email = payload.email.strip().lower()
    existing = db.query(User).filter(User.email == normalized_email).first()
    if existing:
        raise ValueError("Email sudah terdaftar. Silakan gunakan email lain atau login.")

    user_id = f"USR_{uuid4().hex[:10]}"
    new_user = User(
        id=user_id,
        name=payload.name.strip(),
        email=normalized_email,
        hashed_password=hash_password(payload.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return DietMateUser(id=new_user.id, name=new_user.name, email=new_user.email)


def authenticate_user(db: Session, payload: LoginPayload) -> AuthResult:
    """Validasi login pengguna dan mengembalikan status onboarding akun"""
    normalized_email = payload.email.strip().lower()
    user = db.query(User).filter(User.email == normalized_email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise ValueError("Email atau kata sandi yang Anda masukkan salah.")

    progress = get_user_account_progress(db, user.id)
    return AuthResult(
        user=DietMateUser(id=user.id, name=user.name, email=user.email),
        progress=progress,
        access_token=create_access_token(user.id),
    )