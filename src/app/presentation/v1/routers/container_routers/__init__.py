from fastapi import APIRouter

from .proxmox_router import get_proxmox_router


def setup_container_routers(app: APIRouter) -> None:
    app.include_router(get_proxmox_router())
