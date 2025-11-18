#!/usr/bin/env python
"""Initialize database with tables"""
import asyncio
import sys
import os

# Set SQLite mode
os.environ["USE_SQLITE"] = "true"

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.infrastructure.models.user import UserModel
from app.infrastructure.models.project import ProjectModel
from app.infrastructure.models.table import TableModel, ColumnModel
from app.infrastructure.models.cell import RowModel, CellModel
from app.infrastructure.models.version import VersionModel


async def init_db():
    """Create all tables"""
    from app.core.database import engine
    
    async with engine.begin() as conn:
        # Drop all tables (for development)
        await conn.run_sync(Base.metadata.drop_all)
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    
    print("OK: Database initialized successfully!")
    print("OK: All tables created")


if __name__ == "__main__":
    asyncio.run(init_db())

