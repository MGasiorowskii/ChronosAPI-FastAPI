from sqlmodel import create_engine

from core.config import settings

engine = create_engine(str(settings.DATABASE_URI), echo=True, future=True)