from pydantic_settings import BaseSettings


class ProxmoxSettings(BaseSettings):
    BASE_URL: str = 'https://proxmox.nv-server.online/'
    VERIFY_SSL: bool = False

    API_TOKEN_ID: str
    API_TOKEN_SECRET: str

    TIMEOUT: int = 30


    class Config:
        env_file = '.env'
        env_prefix = "PROXMOX_"
        extra = 'ignore'
