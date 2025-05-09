from logging import getLogger

from aiogram import Bot

from .instance_bot import create_bot

logger = getLogger(__name__)


class BotManager:
    def __init__(self, webhook_url: str, token: str):
        self.webhook_url = webhook_url
        self.token = token
        logger.info('Init Bot Manager')

    async def create_bot(self):
        self.bot = create_bot(self.token)
        #await self._configure_webhook(self.bot)

    async def _configure_webhook(self, bot: Bot):
        webhook_url = self.webhook_url

        await bot.delete_webhook(drop_pending_updates=True)
        await bot.set_webhook(webhook_url, allowed_updates=['message', 'callback_query'])
        logger.info(f"Webhook configured for bot {bot.id}")

        return True
