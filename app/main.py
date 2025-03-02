import secrets

from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from api.health_check import router as health_check_router
from api.v1 import urls as v1_urls

from core.config import settings


def custom_generate_unique_id(route: APIRoute) -> str:
    return route.name


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.add_middleware(SessionMiddleware, secret_key=secrets.token_hex(32))


app.include_router(health_check_router)
app.include_router(v1_urls.router)


if settings.ENVIRONMENT != "prod":
    from core.db import engine
    from sqladmin import Admin
    from api.admin import generate_admin_views

    admin = Admin(app, engine)
    generate_admin_views(admin)
