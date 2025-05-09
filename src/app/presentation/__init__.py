from .v1 import VERSION_API, setup_middlewares, setup_routers

SELECT_VERSION_API = VERSION_API


__all__ = [
    'setup_middlewares',
    'setup_routers',
    'SELECT_VERSION_API'
]
