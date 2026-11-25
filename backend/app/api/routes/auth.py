from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.core.security import create_access_token
from app.models.user import User
from app.schemas.auth import (
    AuthResult,
    DietMateUser,
    LoginPayload,
    MessageResponse,
    RegisterPayload,
    RegisterResponse,
)
from app.services.auth_service import (
    authenticate_user,
    get_user_account_progress,
    register_user,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrasi akun baru DietMate",
)
def register(payload: RegisterPayload, db: Session = Depends(get_db)):
    try:
        user = register_user(db, payload)
        return RegisterResponse(user=user, access_token=create_access_token(user.id))
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.post(
    "/login",
    response_model=AuthResult,
    summary="Login akun pengguna DietMate",
)
def login(payload: LoginPayload, db: Session = Depends(get_db)):
    try:
        return authenticate_user(db, payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc


@router.post(
    "/logout",
    response_model=MessageResponse,
    summary="Logout akun pengguna",
)
def logout():
    # Token bersifat stateless: logout dilakukan dengan menghapus token di sisi client.
    return MessageResponse(message="Berhasil logout dari sesi aktif.")


@router.get(
    "/me",
    response_model=AuthResult,
    summary="Data akun & progress onboarding dari token aktif",
)
def me(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return AuthResult(
        user=DietMateUser(id=user.id, name=user.name, email=user.email),
        progress=get_user_account_progress(db, user.id),
        access_token=create_access_token(user.id),
    )
