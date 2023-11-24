from aiogram.types import InlineKeyboardButton

choose1 = InlineKeyboardButton(text="Управление ЖКХ и Обслуживание Дома", callback_data="choose1")
choose2 = InlineKeyboardButton(text="Безопасность и Охрана", callback_data="choose2")
choose3 = InlineKeyboardButton(text="Тарифы и Платежи", callback_data="choose3")
choose4 = InlineKeyboardButton(text="Коммуникация и Взаимодействие", callback_data="choose4")
report_retry = InlineKeyboardButton(text="Повторить заполнение", callback_data="button_reports")
report_accept = InlineKeyboardButton(text="Подтвердить заполнение", callback_data="accept_problem")

