from aiogram.filters.callback_data import CallbackData


class ContainerCallData(CallbackData, prefix='container'):
    action: str
    vmid: int = 0
