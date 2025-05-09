from app.config import create_settings

from .proxmox_provider import ProxmoxProvider


def create_provider() -> ProxmoxProvider:
    settings = create_settings().proxmox_settings
    return ProxmoxProvider(settings)
