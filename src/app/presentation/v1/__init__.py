from .middlewares import setup_middlewares
from .routers import setup_routers

VERSION_API = 'v1'

__all__ = [
    'setup_middlewares',
    'setup_routers',
    'VERSION_API'
]
