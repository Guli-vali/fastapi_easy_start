from fastapi import FastAPI
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware

from app.api.routes.api import router as api_router
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.api.services.users import auth_backend, current_active_user, fastapi_users
from app.core.config import settings


def setup_3rd_parties(application: FastAPI) -> None:
    add_pagination(application)

def setup_middlewaries(application: FastAPI, settings: AppSettings) -> None:
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def setup_routes(application: FastAPI, settings: AppSettings)-> None:

    @application.get(
        '/',
        name="core:healthcheck"
    )
    def healthchek():
        return {"ping": "pong"}

    application.include_router(api_router, prefix=settings.api_prefix)
    application.include_router(
        fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
    )
    application.include_router(fastapi_users.get_register_router(), prefix="/auth", tags=["auth"])
    application.include_router(
        fastapi_users.get_reset_password_router(),
        prefix="/auth",
        tags=["auth"],
    )
    application.include_router(
        fastapi_users.get_verify_router(),
        prefix="/auth",
        tags=["auth"],
    )
    application.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])


def get_application(settings: AppSettings) -> FastAPI:

    application = FastAPI(**settings.fastapi_kwargs)

    setup_routes(application, settings)
    setup_3rd_parties(application)
    setup_middlewaries(application, settings)

    return application


app = get_application(settings)
