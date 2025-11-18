"""
Database session management
"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import get_settings
import os

settings = get_settings()

# Determine database URL - use SQLite for development if PostgreSQL not available
database_url = settings.DATABASE_URL

# Check if we should use SQLite (for development without PostgreSQL)
if os.getenv("USE_SQLITE", "false").lower() == "true" or "postgresql" not in database_url.lower():
    # Use SQLite for development
    database_url = "sqlite+aiosqlite:///./gdh.db"
    engine = create_async_engine(
        database_url,
        echo=settings.DATABASE_ECHO,
        future=True,
        connect_args={"check_same_thread": False}  # SQLite specific
    )
else:
    # Use PostgreSQL
    engine = create_async_engine(
        database_url.replace("postgresql://", "postgresql+asyncpg://"),
        echo=settings.DATABASE_ECHO,
        future=True,
    )

# Create session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base class for models
Base = declarative_base()


async def get_db() -> AsyncSession:
    """
    Dependency for getting database session
    Yields a database session and ensures it's closed after use
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

