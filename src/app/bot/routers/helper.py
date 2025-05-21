from contextlib import suppress

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)


async def edit_message(
        event: CallbackQuery | Message,
        text: str | None = None,
        reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | None = None,
        photo = None, **kwargs
    ):
    if isinstance(event, CallbackQuery):
        message = event.message
    elif isinstance(event, Message):
        message = event
    else:
        raise Exception('H1!!')
    if not isinstance(message, Message):
        raise Exception('H1!!')

    try:
        if photo:
            media = InputMediaPhoto(media=photo, caption=text)
            return await message.edit_media(media, reply_markup=reply_markup) # type: ignore
        else:
            return await message.edit_text(text=text, reply_markup=reply_markup, **kwargs) # type: ignore
    except TelegramBadRequest as e:
        if 'message is not modified' in str(e):
            return

    with suppress(Exception):
        if isinstance(event, CallbackQuery):
            await message.delete()
    if photo:
        with suppress(Exception):
            return await message.answer_photo(photo=photo, caption=text, reply_markup=reply_markup, **kwargs)
    return await message.answer(text=text, reply_markup=reply_markup, **kwargs)  # type: ignore
