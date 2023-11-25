from aiogram.types import InlineKeyboardButton

register = InlineKeyboardButton(text="Зарегистрироваться", callback_data="register")
button_requests = InlineKeyboardButton(text="Заявки", callback_data="button_requests")
button_reports = InlineKeyboardButton(text="Жалобы", callback_data="button_reports")
button_faq = InlineKeyboardButton(text="F.A.Q (Частые вопросы)", url="https://telegra.ph/CHasto-zadavaemye-voprosy-11-23-4")
exit_from_account = InlineKeyboardButton(text="Выйти из аккаунта", callback_data="exit_from_account")
accept_exit = InlineKeyboardButton(text="Подтвердить", callback_data="accept_exit")
decline_exit = InlineKeyboardButton(text="Отменить", callback_data="start")
user_to_house = InlineKeyboardButton(text="Закрепиться за домом", callback_data="user_to_house")
go_to_bot = InlineKeyboardButton(text="Перейти в бота", url="https://t.me/rostelekom_key_bot")


user_menu = InlineKeyboardButton(text="Пользовательское меню", callback_data="start")

