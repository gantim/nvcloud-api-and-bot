from fastapi import FastAPI

from .cors_middlewares import connect_cors_middlewares


def setup_middlewares(app: FastAPI) -> None:
    connect_cors_middlewares(app)
