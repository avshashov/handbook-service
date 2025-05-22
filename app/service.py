from fastapi import FastAPI

from app.api.router import main_router
from app.middleware import APIKeyMiddleware
from config import settings


class HandbookService:
    _instance = None

    def __new__(cls, *args, **kwargs) -> 'HandbookService':
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        self.__app = self.__init_app()

    @staticmethod
    def __init_app() -> FastAPI:
        app = FastAPI()
        if settings.authentication.enabled:
            app.add_middleware(APIKeyMiddleware, app_key=settings.authentication.api_key.get_secret_value())
        app.include_router(router=main_router)
        return app

    @property
    def app(self) -> FastAPI:
        return self.__app


handbook_service = HandbookService()
