from aiogram.types import InlineKeyboardButton

admin_panel = InlineKeyboardButton(text="Панель Администратора", callback_data="admin")
back = InlineKeyboardButton(text="Назад", callback_data="admin")
add_house = InlineKeyboardButton(text="Добавить дом", callback_data="add_house")
admin_request = InlineKeyboardButton(text="Все верно", callback_data="admin_request")
add_admin = InlineKeyboardButton(text="Добавить администратора", callback_data="add_admin")