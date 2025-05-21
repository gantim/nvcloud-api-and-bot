from aiogram.types import InlineKeyboardMarkup, WebAppInfo

from app.bot.callback_data.container import ContainerCallData
from app.bot.keyboards.inline.base import InlineKeyboardsBase


class PrivateInlineKeyboards(InlineKeyboardsBase):
    @classmethod
    def start(cls) -> InlineKeyboardMarkup:
        builder = cls()
        builder.button(text='🌐 Веб-приложение', web_app=WebAppInfo(url='https://cloud.nv-server.online'))
        builder.button(text='📊 Контейнеры', callback_data='containers')
        builder.button(text='🛠 Поддержка', callback_data='support')

        return builder.adjust(1, 2).as_markup() # type: ignore

    @classmethod
    def auth(cls) -> InlineKeyboardMarkup:
        builder = cls()
        builder.button(text='🌐 Авторизоваться', web_app=WebAppInfo(url='https://cloud.nv-server.online'))

        return builder.as_markup() # type: ignore

    @classmethod
    def containers(cls, containers: dict[int, str]):
        builder = cls()

        for vmid, host_name in containers.items():
            builder.button(text=host_name, callback_data=ContainerCallData(action='select', vmid=vmid))

        builder.button(text='Назад', callback_data='menu')

        return builder.adjust(1).as_markup()

    @classmethod
    def container_telemetry(cls, vmid: int):
        builder = cls()

        builder.button(text='🔄 Обновить', callback_data=ContainerCallData(action='update', vmid=vmid))
        builder.button(text='Назад', callback_data='containers')

        return builder.adjust(1).as_markup()

    @classmethod
    def support(cls):
        builder = cls()

        builder.button(text='Назад', callback_data='menu')

        return builder.adjust(1).as_markup()
