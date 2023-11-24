from aiogram.types import InlineKeyboardButton

register = InlineKeyboardButton(text="Зарегистрироваться", callback_data="register")
button_member_chats = InlineKeyboardButton(text="Чаты жильцов", callback_data="button_member_chats")
button_requests = InlineKeyboardButton(text="Заявки", callback_data="button_requests")
button_reports = InlineKeyboardButton(text="Жалобы", callback_data="button_reports")
button_faq = InlineKeyboardButton(text="F.A.Q (Частые вопросы)", callback_data="button_faq")
exit_from_account = InlineKeyboardButton(text="Выйти из аккаунта", callback_data="exit_from_account")
accept_exit = InlineKeyboardButton(text="Подтвердить", callback_data="accept_exit")
decline_exit = InlineKeyboardButton(text="Отменить", callback_data="start")
user_menu = InlineKeyboardButton(text="Пользовательское меню", callback_data="start")

