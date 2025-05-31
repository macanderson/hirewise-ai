import asyncio
import importlib.util
import os
from pathlib import Path

os.environ.setdefault("JWT_SECRET", "test-secret")

auth_path = Path(__file__).resolve().parents[1] / "src/api/services/auth.py"
spec = importlib.util.spec_from_file_location("auth", auth_path)
auth = importlib.util.module_from_spec(spec)
spec.loader.exec_module(auth)
AuthService = auth.AuthService


async def _hash(service: AuthService, password: str) -> str:
    return await service.hash_password(password)


async def _verify(service: AuthService, password: str, hashed: str) -> bool:
    return await service.verify_password(password, hashed)


def test_hash_password_produces_unique_hashes():
    service = AuthService()
    password = "secret-password"

    hashed1 = asyncio.run(_hash(service, password))
    hashed2 = asyncio.run(_hash(service, password))

    assert hashed1 != password
    assert hashed2 != password
    assert hashed1 != hashed2
    assert len(hashed1) >= 60
    assert len(hashed2) >= 60


def test_verify_password_succeeds_for_correct_password():
    service = AuthService()
    password = "another-secret"
    hashed = asyncio.run(_hash(service, password))

    assert asyncio.run(_verify(service, password, hashed)) is True


def test_verify_password_fails_for_wrong_password():
    service = AuthService()
    password = "correct-password"
    wrong_password = "wrong-password"
    hashed = asyncio.run(_hash(service, password))

    assert asyncio.run(_verify(service, wrong_password, hashed)) is False
