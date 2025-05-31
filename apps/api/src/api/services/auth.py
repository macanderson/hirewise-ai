import logging
from datetime import datetime, timedelta
from typing import Optional

import bcrypt
from jose import JWTError, jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from api.core.config import settings

try:
    from supabase import create_client, Client
except Exception:  # pragma: no cover
    Client = None
    create_client = None

logger = logging.getLogger(__name__)


class AuthService:
    """Authentication service wrapping Supabase auth."""

    def __init__(self) -> None:
        self.JWT_SECRET = settings.JWT_SECRET
        self.algorithm = "HS256"
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.supabase: Optional[Client] = None
        if create_client is not None:
            try:
                self.supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
            except Exception as exc:  # pragma: no cover
                logger.warning("Failed to create Supabase client: %s", exc)

    async def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

    async def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=self.access_token_expire_minutes))
        to_encode = {**data, "exp": expire}
        return jwt.encode(to_encode, self.JWT_SECRET, algorithm=self.algorithm)

    async def decode_access_token(self, token: str) -> Optional[dict]:
        try:
            return jwt.decode(token, self.JWT_SECRET, algorithms=[self.algorithm], options={"verify_exp": True})
        except JWTError:
            return None

    async def sign_up(self, email: str, password: str, **metadata) -> dict:
        if not self.supabase:
            raise RuntimeError("Supabase client not configured")
        res = await self.supabase.auth.sign_up({"email": email, "password": password, "data": metadata})
        if not res or not res.session:
            raise ValueError("Registration failed")
        return {"access_token": res.session.access_token, "token_type": "bearer"}

    async def login(self, email: str, password: str) -> dict:
        if not self.supabase:
            raise RuntimeError("Supabase client not configured")
        res = await self.supabase.auth.sign_in_with_password({"email": email, "password": password})
        if not res or not res.session:
            raise ValueError("Invalid email or password")
        return {"access_token": res.session.access_token, "token_type": "bearer"}

    async def get_current_user(self, token: str):
        if not self.supabase:
            raise RuntimeError("Supabase client not configured")
        res = await self.supabase.auth.get_user(token)
        return res.user if res else None

    async def logout(self, token: str) -> None:
        if not self.supabase:
            raise RuntimeError("Supabase client not configured")
        await self.supabase.auth.sign_out()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_auth_service() -> AuthService:
    return AuthService()


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.get_current_user(token)
