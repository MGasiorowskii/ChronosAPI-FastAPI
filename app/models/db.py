from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine

from core.config import settings

engine = AsyncEngine(create_engine(str(settings.DATABASE_URI), echo=True, future=True))
