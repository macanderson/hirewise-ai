import logging
from contextlib import asynccontextmanager

import uvicorn

from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.core.config import settings
from api.routes.v1 import router as v1_router
from api.services.auth import AuthService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Initialize logger
logger = logging.getLogger(__name__)


# Initialize auth service
auth_service = AuthService()


def start():
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan."""
    yield



app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    license_info={
        "name": settings.PROJECT_LICENSE,
        "url": settings.PROJECT_LICENSE_URL,
    },
    contact={
        "name": settings.PROJECT_NAME,
        "url": settings.PROJECT_URL,
    },
    lifespan=lifespan,
    swagger_ui_oauth2_redirect_url=f"{settings.API_V1_STR}/auth/login",
    openapi_tags=[
        {
            "name": "auth",
            "description": "Operations related to authentication."
        },
        {
            "name": "users",
            "description": "Operations related to users."
        },
        # Add more tags as needed
    ],
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register routers
app.include_router(
    v1_router,
    prefix=f"{settings.API_V1_STR}",
    tags=["v1"],
)


@app.get(f"{settings.API_V1_STR}/health")
async def health_check():
    return {"status": "healthy"}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "flows": {
                "password": {
                    "tokenUrl": f"{settings.API_V1_STR}/auth/login",
                    "scopes": {

                    },
                }
            },
        }
    }
    openapi_schema["security"] = [{"OAuth2PasswordBearer": []}]
    openapi_schema["servers"] = [{"url": "http://localhost:8000"}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    start()
