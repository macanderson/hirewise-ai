from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr

from api.services.auth import AuthService, get_current_user

router = APIRouter()

auth_service = AuthService()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


class Token(BaseModel):
    access_token: str
    token_type: str


class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    organization_name: Optional[str] = None


@router.post("/sign-up", response_model=Token)
async def sign_up(data: SignUpRequest):
    try:
        return await auth_service.sign_up(
            data.email,
            data.password,
            first_name=data.first_name,
            last_name=data.last_name,
            organization=data.organization_name,
        )
    except Exception as exc:  # pragma: no cover - external service
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        return await auth_service.login(form_data.username, form_data.password)
    except Exception as exc:  # pragma: no cover - external service
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))


@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    await auth_service.logout(token)
    return {"message": "Successfully logged out"}


@router.get("/me")
async def me(user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return user
