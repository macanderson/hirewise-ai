import logging
from contextlib import asynccontextmanager

import uvicorn

from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from api.db.client import get_prisma_client
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
    """
    Lifespan for the FastAPI application.

    This function is used to initialize the Prisma client
    and connect to the database.
    """
    # Startup
    # Initialize Prisma client
    prisma = get_prisma_client()
    await prisma.connect()
    yield
    # Shutdown
    await auth_service.prisma.disconnect()


class TenantMiddleware(BaseHTTPMiddleware):
    """
    Tenant middleware.

    This middleware is used to check if the tenant ID
    is provided in the request headers. If not, it will
    return a 400 error.

    If the tenant ID is provided, it will store the tenant
    ID in the request state for later use.

    If the tenant ID is not provided, it will skip the
    tenant check and continue processing the request.

    If the tenant ID is provided, it will check if the tenant
    exists in the database. If the tenant does not exist,
    it will return a 404 error. If the tenant exists, it will
    continue processing the request.
    """

    async def dispatch(self, request: Request, call_next):
        """
        Dispatch the request.

        This method is used to dispatch the request to the next middleware.
        """
        tenant_id = request.headers.get("X-Tenant-Id")

        # Skip tenant check for auth endpoints and public routes
        if (request.url.path.startswith(f"{settings.API_V1_STR}/auth/login") or  # noqa: E501
                request.url.path.startswith(
                    f"{settings.API_V1_STR}/auth/register"
                ) or  # noqa: E501
                request.url.path.startswith(
                    f"{settings.API_V1_STR}/auth/verify-email"
                ) or  # noqa: E501
                request.url.path.startswith(
                    f"{settings.API_V1_STR}/auth/reset-password"
                ) or  # noqa: E501
                request.url.path.startswith(
                    f"{settings.API_V1_STR}/auth/reset-password-confirm"
                ) or  # noqa: E501
                request.url.path.startswith(
                    f"{settings.API_V1_STR}/auth/refresh-token"
                ) or  # noqa: E501
                request.url.path.startswith(f"{settings.API_V1_STR}/auth/logout") or  # noqa: E501
                request.url.path.startswith(f"{settings.API_V1_STR}/docs") or  # noqa: E501
                request.url.path.startswith(f"{settings.API_V1_STR}/redoc") or  # noqa: E501
                request.url.path.startswith(f"{settings.API_V1_STR}/openapi.json") or  # noqa: E501
                request.url.path.startswith(f"{settings.API_V1_STR}/health")):  # noqa: E501
            logger.info(f"Skipping tenant check for {request.url.path}")
            return await call_next(request)

        # For protected routes, ensure tenant ID is provided
        if not tenant_id:
            return Response(
                status_code=400,
                content="X-Tenant-Id header is required",
                media_type="text/plain",
            )

        # Store tenant ID in request state for later use
        request.state.tenant_id = tenant_id

        # Continue processing the request
        return await call_next(request)


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

# Add tenant middleware
app.add_middleware(TenantMiddleware)

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
