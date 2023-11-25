from aiogram.types import InlineKeyboardButton

back = InlineKeyboardButton(text="Назад", callback_data="start")
request_retry = InlineKeyboardButton(text="Повторить заполнение", callback_data="button_requests")
request_accept = InlineKeyboardButton(text="Направить на модерацию", callback_data="accept_request")
