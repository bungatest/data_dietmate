from pydantic import BaseModel, EmailStr, Field


class RegisterPayload(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)


class LoginPayload(BaseModel):
    email: EmailStr
    password: str


class DietMateUser(BaseModel):
    id: str
    name: str
    email: str


class AccountProgress(BaseModel):
    profile_completed: bool = False
    preferences_completed: bool = False
    has_meal_plan: bool = False


class AuthResult(BaseModel):
    user: DietMateUser
    progress: AccountProgress


class RegisterResponse(BaseModel):
    user: DietMateUser


class MessageResponse(BaseModel):
    message: str