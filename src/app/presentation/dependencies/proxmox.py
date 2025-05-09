from contextlib import asynccontextmanager
from typing import AsyncIterator

from app.infra.proxmox import create_provider
from app.infra.proxmox.proxmox_provider import ProxmoxProvider


@asynccontextmanager
async def get_proxmox_provider() -> AsyncIterator[ProxmoxProvider]:
    provider = create_provider()
    try:
        await provider._ensure_session()
        yield provider
    finally:
        await provider.close()
