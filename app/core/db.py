import redis
from sqlmodel import create_engine

from core.config import settings

engine = create_engine(str(settings.DATABASE_URI), echo=True, future=True)
pool = redis.ConnectionPool.from_url(str(settings.REDIS_URI), decode_responses=True)

cache = redis.Redis(connection_pool=pool)