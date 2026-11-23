from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.auth import (
    AuthResult,
    LoginPayload,
    MessageResponse,
    RegisterPayload,
    RegisterResponse,
)
from app.services.auth_service import authenticate_user, register_user

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
        return RegisterResponse(user=user)
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
    return MessageResponse(message="Berhasil logout dari sesi aktif.")