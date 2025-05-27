from fastapi import APIRouter

from api.routes.v1.agents import router as agents_router
from api.routes.v1.auth import router as auth_router
from api.routes.v1.chats import router as chats_router
from api.routes.v1.documents import router as documents_router
from api.routes.v1.projects import router as projects_router
from api.routes.v1.tenants import router as tenants_router
from api.routes.v1.users import router as users_router

router = APIRouter()
router.include_router(agents_router, prefix="/agents", tags=["agents"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(chats_router, prefix="/chats", tags=["chats"])
router.include_router(documents_router, prefix="/documents", tags=["documents"])
router.include_router(projects_router, prefix="/projects", tags=["projects"])
router.include_router(tenants_router, prefix="/tenants", tags=["tenants"])
router.include_router(users_router, prefix="/users", tags=["users"])

__all__ = ["router"]
