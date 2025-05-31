"""
Database client module for managing Prisma
connections and transactions.

This module provides a singleton Prisma client and utilities
for database operations.
"""

import logging
from contextlib import asynccontextmanager
from functools import lru_cache
from typing import AsyncGenerator, Optional

try:
    from database.client import Prisma
except Exception:  # pragma: no cover - fallback when Prisma isn't installed
    class _ModelStub:
        async def find_unique(self, *args, **kwargs):
            raise NotImplementedError("Prisma model access is unavailable")

        async def find_first(self, *args, **kwargs):
            raise NotImplementedError("Prisma model access is unavailable")

        async def find_many(self, *args, **kwargs):
            raise NotImplementedError("Prisma model access is unavailable")

        async def create(self, *args, **kwargs):
            raise NotImplementedError("Prisma model access is unavailable")

        async def update(self, *args, **kwargs):
            raise NotImplementedError("Prisma model access is unavailable")

        async def update_many(self, *args, **kwargs):
            raise NotImplementedError("Prisma model access is unavailable")

    class Prisma:  # pragma: no cover - minimal stub
        def __init__(self) -> None:
            self._connected = False

        async def connect(self) -> None:
            self._connected = True

        async def disconnect(self) -> None:
            self._connected = False

        def is_connected(self) -> bool:
            return self._connected

        async def query_raw(self, *args, **kwargs):
            raise NotImplementedError("Raw queries are unavailable")

        def tx(self):
            raise NotImplementedError("Transactions are unavailable")

        def __getattr__(self, name: str) -> _ModelStub:
            return _ModelStub()

logger = logging.getLogger(__name__)

# Global Prisma client instance
_prisma_client: Optional[Prisma] = None


@lru_cache()
def get_prisma_client() -> Prisma:
    """
    Get a singleton instance of the Prisma client.

    This function uses LRU cache to ensure only one instance is created
    per application lifecycle.

    Returns:
        Prisma: A singleton instance of the Prisma client
    """
    global _prisma_client
    if _prisma_client is None:
        _prisma_client = Prisma()
        logger.debug("Created new Prisma client instance")
    return _prisma_client


@asynccontextmanager
async def get_database_connection() -> AsyncGenerator[Prisma, None]:  # noqa: E501
    """
    Context manager for handling Prisma client connections.

    This ensures proper connection/disconnection lifecycle and should be used
    for operations that need guaranteed connection cleanup.

    Example:
        async with get_database_connection() as db:
            user = await db.user.find_unique(where={"id": user_id})

    Yields:
        Prisma: A connected Prisma client instance
    """
    client = get_prisma_client()
    if not client.is_connected():
        await client.connect()
        logger.debug("Connected to database")

    try:
        yield client
    except Exception as e:
        logger.error(f"Database operation error: {e}")
        raise
    finally:
        # Note: We don't disconnect here as we're using a singleton
        # The connection will be managed by the application lifecycle
        pass


@asynccontextmanager
async def get_database_transaction() -> AsyncGenerator[Prisma, None]:
    """
    Context manager for database transactions.

    This provides a transactional context where all operations either
    succeed together or fail together.

    Example:
        async with get_database_transaction() as tx:
            await tx.user.create(data={"email": "test@example.com"})
            await tx.project.create(data={"name": "Test Project"})
            # Both operations succeed or both fail

    Yields:
        TransactionManager: A transaction manager for database operations
    """
    client = get_prisma_client()
    if not client.is_connected():
        await client.connect()
        logger.debug("Connected to database for transaction")

    async with client.tx() as tx:
        logger.debug("Started database transaction")
        try:
            yield tx
            logger.debug("Transaction completed successfully")
        except Exception as e:
            logger.error(f"Transaction failed: {e}")
            raise


async def connect_database() -> None:
    """
    Connect to the database.

    This should be called during application startup.
    """
    client = get_prisma_client()
    if not client.is_connected():
        await client.connect()
        logger.info("Connected to database")
    else:
        logger.debug("Database already connected")


async def disconnect_database() -> None:
    """
    Disconnect from the database.

    This should be called during application shutdown.
    """
    client = get_prisma_client()
    if client.is_connected():
        await client.disconnect()
        logger.info("Disconnected from database")
    else:
        logger.debug("Database already disconnected")


async def check_database_health() -> bool:
    """
    Check if the database connection is healthy.

    Returns:
        bool: True if database is accessible, False otherwise
    """
    try:
        client = get_prisma_client()
        if not client.is_connected():
            await client.connect()

        # Simple query to test connection
        await client.query_raw("SELECT 1")
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False


class DatabaseError(Exception):
    """Base exception for database-related errors."""
    pass


class DatabaseConnectionError(DatabaseError):
    """Exception raised when database connection fails."""
    pass


class DatabaseTransactionError(DatabaseError):
    """Exception raised when database transaction fails."""
    pass
