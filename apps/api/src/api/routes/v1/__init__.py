from fastapi import APIRouter

from api.routes.v1.auth import router as auth_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["auth"])

__all__ = ["router"]
