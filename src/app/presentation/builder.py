from fastapi import FastAPI
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from app.config.api import APISettings
from app.presentation import setup_middlewares, setup_routers
from app.presentation.exceptions import setup_exception_handlers


class APIBuilder:
    def __init__(self, settings: APISettings, lifespan) -> None:
        self.settings = settings
        self.api = self._create_api_instance(lifespan)

    def _create_api_instance(self, lifespan) -> FastAPI:
        return FastAPI(
            debug=self.settings.DEBUG,
            title=self.settings.TITLE,
            description=self.settings.DESCRIPTION,
            version=self.settings.VERSION,
            lifespan=lifespan
        )

    def add_dependency_override(self, _cls, obj):
        self.api.dependency_overrides[_cls] = lambda: obj

    def configure_middlewares(self) -> None:
        self.api.add_middleware(ProxyHeadersMiddleware, trusted_hosts=["*"])
        setup_middlewares(self.api)

    def configure_routers(self) -> None:
        setup_routers(self.api)

    def configure_exceptions(self) -> None:
        setup_exception_handlers(self.api)

    def build(self) -> FastAPI:
        self.configure_exceptions()
        self.configure_middlewares()
        self.configure_routers()
        return self.api

def get_api_builder(settings: APISettings, lifespan):
    builder = APIBuilder(settings, lifespan)
    return builder
