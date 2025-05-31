import logging
from datetime import datetime, timedelta
from typing import Optional

import bcrypt
from jose import JWTError, jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from supabase import create_client, Client

from api.core.config import settings


logger = logging.getLogger(__name__)


class AuthService:
    """Authentication service wrapping Supabase auth."""  # noqa: E501

    def __init__(self) -> None:
        self.JWT_SECRET = settings.JWT_SECRET  # noqa: E501
        self.algorithm = "HS256"
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES  # noqa: E501
        self.supabase: Optional["Client"] = None  # noqa: E501
        if create_client is not None:
            try:
                # fmt: off
                self.supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)  # noqa: E501
                # fmt: on
            except Exception as exc:  # pragma: no cover
                logger.warning("Failed to create Supabase client: %s", exc)  # noqa: E501

    async def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:  # noqa: E501
        # fmt: off
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))  # noqa: E501
        # fmt: on

    async def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        # fmt: off
        expire = datetime.utcnow() + (
            expires_delta or
            timedelta(minutes=self.access_token_expire_minutes)
        )
        # fmt: on
        to_encode = {**data, "exp": expire}
        return jwt.encode(to_encode, self.JWT_SECRET, algorithm=self.algorithm)  # noqa: E501

    async def decode_access_token(self, token: str) -> Optional[dict]:  # noqa: E501
        try:
            # fmt: off
            return jwt.decode(token, self.JWT_SECRET, algorithms=[self.algorithm], options={"verify_exp": True})  # noqa: E501
            # fmt: on
        except JWTError:
            return None

    async def sign_up(self, email: str, password: str, **metadata) -> dict:  # noqa: E501    # noqa: E501
        if not self.supabase:
            raise RuntimeError("Supabase client not configured")  # noqa: E501
        # fmt: off
        res = await self.supabase.auth.sign_up({"email": email, "password": password, "data": metadata})  # noqa: E501
        # fmt: on
        if not res or not res.session:
            raise ValueError("Registration failed")  # noqa: E501
        # fmt: off
        return {"access_token": res.session.access_token, "token_type": "bearer"}  # noqa: E501
        # fmt: on

    async def login(self, email: str, password: str) -> dict:  # noqa: E501
        if not self.supabase:
            raise RuntimeError("Supabase client not configured")  # noqa: E501
        # fmt: off
        res = await self.supabase.auth.sign_in_with_password({"email": email, "password": password})  # noqa: E501
        # fmt: on
        if not res or not res.session:
            raise ValueError("Invalid email or password")  # noqa: E501
        # fmt: off
        return {"access_token": res.session.access_token, "token_type": "bearer"}  # noqa: E501
        # fmt: on

    async def get_current_user(self, token: str):  # noqa: E501
        if not self.supabase:
            raise RuntimeError("Supabase client not configured")  # noqa: E501
        res = await self.supabase.auth.get_user(token)  # noqa: E501
        return res.user if res else None  # noqa: E501

    async def logout(self, token: str) -> None:  # noqa: E501
        if not self.supabase:
            raise RuntimeError("Supabase client not configured")  # noqa: E501
        await self.supabase.auth.sign_out()  # noqa: E501


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")  # noqa: E501


def get_auth_service() -> AuthService:  # noqa: E501
    return AuthService()  # noqa: E501


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),  # noqa: E501
):  # noqa: E501
    return await auth_service.get_current_user(token)  # noqa: E501
