from typing import TYPE_CHECKING

from aiogram import F
from aiogram.enums.chat_type import ChatType
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, FSInputFile, Message, User

from app.bot.callback_data.container import ContainerCallData
from app.bot.keyboards.inline.private.private_keyboards import PrivateInlineKeyboards
from app.bot.locales import ru
from app.bot.routers import BaseRouter
from app.bot.routers.helper import edit_message
from app.domain.models.tg_user import TgUserInDB
from app.domain.models.user import UserInDB

if TYPE_CHECKING:
    from app.domain.services.container import ContainerService


class UserRouter(BaseRouter):
    chat_types = ChatType.PRIVATE

    def setup_handlers(self):
        @self.message(CommandStart())
        @self.callback_query(F.data == 'menu')
        async def start_handler(event: Message | CallbackQuery, user_in_db: UserInDB, user: TgUserInDB, event_from_user: User):
            if user:
                text = ru.START_TEXT_WITH_AUTH.format(full_name=user_in_db.username)
                keyboard = PrivateInlineKeyboards.start()
                photo = FSInputFile('app/public/PostMessage_5.png')
            else:
                text = ru.START_TEXT_WITHOUT_AUTH.format(full_name=event_from_user.full_name)
                keyboard = PrivateInlineKeyboards.auth()
                photo = FSInputFile('app/public/PostMessage_0.png')
            await edit_message(event, text, keyboard, photo)

        @self.callback_query(F.data == 'containers')
        async def containers_hadler(event: CallbackQuery, container_service: 'ContainerService'):
            containers = await container_service.get_containers()

            kb_labels = {
                container.id:
                f'{'🟢' if container.status == 'running' else '🔴'} {container.name}'
                for container in containers
            }
            text = ru.CONTAINERS_TEXT
            keyboard = PrivateInlineKeyboards.containers(kb_labels)

            await edit_message(event, text, keyboard, FSInputFile('app/public/PostMessage_4.png'))

        @self.callback_query(ContainerCallData.filter(F.action.in_(['select', 'update'])))
        async def telemetry_container_handler(event: CallbackQuery, container_service: 'ContainerService', callback_data: ContainerCallData):
            vmid = int(callback_data.vmid)
            container_telemetry =  await container_service.get_telemetry_container(vmid)
            await event.answer()
            if container_telemetry:
                text = ru.CONTAINER_TELEMETRY_TEXT.format(
                    name=container_telemetry.container.name,
                    id=container_telemetry.container.id,
                    status='🟢' if container_telemetry.container.status == 'running' else '🔴',

                    cpu_cores=container_telemetry.cpu.cpu_cores,
                    busy_cpu=f'{100-container_telemetry.cpu.free_cpu*100:.1f}',

                    ram_total=container_telemetry.ram.ram_bytes // (1024**2),
                    ram_free=container_telemetry.ram.free_ram_bytes // (1024**2),
                    ram_used=(container_telemetry.ram.ram_bytes - container_telemetry.ram.free_ram_bytes) // (1024**2),

                    rom_total=container_telemetry.rom.rom_bytes // (1024**2),
                    rom_busy=(container_telemetry.rom.rom_bytes - container_telemetry.rom.free_rom_bytes) // (1024**2),

                    net_in_total=container_telemetry.network.incoming_total_bytes // (1024**2),
                    net_out_total=container_telemetry.network.outgoing_total_bytes // (1024**2),
                    net_in_current=container_telemetry.network.incoming_current_bytes // 1024,
                    net_out_current=container_telemetry.network.outgoing_current_bytes // 1024,

                    username=container_telemetry.user.username,
                    password=container_telemetry.user.password,
                    ssh_connect=f'ssh -p 22{container_telemetry.container.id} {container_telemetry.container.name}.nv-server.online'
                )

                keyboard = PrivateInlineKeyboards.container_telemetry(vmid)

                await edit_message(event, text, keyboard, FSInputFile('app/public/PostMessage_4.png'))

        @self.callback_query(F.data == 'support')
        async def support_handler(event: CallbackQuery):
            text = ru.SUPPORT_TEXT
            keyboard = PrivateInlineKeyboards.support()
            await edit_message(event, text, keyboard, FSInputFile('app/public/PostMessage_3.png'))
