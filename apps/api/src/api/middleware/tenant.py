"""
Tenant-aware middleware for FastAPI.

This middleware ensures that all requests include proper tenant context
and validates tenant access permissions.
"""

import logging
from typing import Callable, Optional

from fastapi import HTTPException, Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware

from api.db.client import get_prisma_client

logger = logging.getLogger(__name__)


class TenantMiddleware(BaseHTTPMiddleware):
    """
    Middleware to handle tenant-aware requests.

    This middleware:
    1. Extracts tenant ID from X-Tenant-Id header
    2. Validates tenant exists and is active
    3. Stores tenant context in request state
    4. Skips validation for public routes
    """

    # Routes that don't require tenant validation
    PUBLIC_ROUTES = {
        "/health",
        "/docs",
        "/redoc",
        "/openapi.json",
    }

    # Route prefixes that don't require tenant validation
    PUBLIC_PREFIXES = {
        "/api/v1/auth",
        "/static",
        "/favicon",
    }

    def __init__(self, app, require_tenant: bool = True):
        """
        Initialize the tenant middleware.

        Args:
            app: The FastAPI application instance
            require_tenant: Whether to require tenant validation (default: True)
        """
        super().__init__(app)
        self.require_tenant = require_tenant

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process the request and validate tenant context.

        Args:
            request: The incoming HTTP request
            call_next: The next middleware or route handler

        Returns:
            Response: The HTTP response
        """
        # Skip tenant validation for public routes
        if self._is_public_route(request.url.path):
            return await call_next(request)

        # Extract tenant ID from header
        tenant_id = request.headers.get("X-Tenant-Id")

        if not tenant_id and self.require_tenant:
            logger.warning(f"Missing X-Tenant-Id header for {request.url.path}")
            return Response(
                status_code=status.HTTP_400_BAD_REQUEST,
                content="X-Tenant-Id header is required",
                media_type="text/plain",
            )

        if tenant_id:
            # Validate tenant exists and is active
            tenant = await self._validate_tenant(tenant_id)
            if not tenant:
                logger.warning(f"Invalid tenant ID: {tenant_id}")
                return Response(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content="Tenant not found or inactive",
                    media_type="text/plain",
                )

            # Store tenant context in request state
            request.state.tenant_id = tenant_id
            request.state.tenant = tenant
            request.state.prisma = get_prisma_client()

            logger.debug(f"Request processed with tenant: {tenant.name} ({tenant_id})")

        # Continue with the request
        return await call_next(request)

    def _is_public_route(self, path: str) -> bool:
        """
        Check if the route is public and doesn't require tenant validation.

        Args:
            path: The request path

        Returns:
            bool: True if the route is public, False otherwise
        """
        # Check exact matches
        if path in self.PUBLIC_ROUTES:
            return True

        # Check prefix matches
        for prefix in self.PUBLIC_PREFIXES:
            if path.startswith(prefix):
                return True

        return False

    async def _validate_tenant(self, tenant_id: str) -> Optional[dict]:
        """
        Validate that the tenant exists and is active.

        Args:
            tenant_id: The tenant ID to validate

        Returns:
            Optional[dict]: The tenant data if valid, None otherwise
        """
        try:
            prisma = get_prisma_client()
            if not prisma.is_connected():
                await prisma.connect()

            tenant = await prisma.tenant.find_unique(
                where={"id": tenant_id},
                include={"license": True}
            )

            # Check if tenant exists and is not deleted
            if not tenant or tenant.deleted_at is not None:
                return None

            return tenant

        except Exception as e:
            logger.error(f"Error validating tenant {tenant_id}: {e}")
            return None


def get_tenant_context(request: Request) -> Optional[dict]:
    """
    Get the tenant context from the request state.

    Args:
        request: The FastAPI request object

    Returns:
        Optional[dict]: The tenant data if available, None otherwise
    """
    return getattr(request.state, "tenant", None)


def get_tenant_id(request: Request) -> Optional[str]:
    """
    Get the tenant ID from the request state.

    Args:
        request: The FastAPI request object

    Returns:
        Optional[str]: The tenant ID if available, None otherwise
    """
    return getattr(request.state, "tenant_id", None)


def require_tenant_context(request: Request) -> dict:
    """
    Get the tenant context and raise an exception if not available.

    Args:
        request: The FastAPI request object

    Returns:
        dict: The tenant data

    Raises:
        HTTPException: If tenant context is not available
    """
    tenant = get_tenant_context(request)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tenant context not available"
        )
    return tenant
