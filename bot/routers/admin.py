import random
import string

from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.texts import admin as admin_texts
from bot.buttons import admin as admin_buttons
from bot.states import admin_states, start_states

from bot.base import dbase

router = Router()


def randomword():
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(10))


@router.message(Command("admin_request"))
async def admin_request(message: Message, state: FSMContext):
    if dbase.admin.is_admin(message.chat.id):
        await message.answer(text=admin_texts.admin_request_from_admin)
    else:
        await message.answer(text=admin_texts.admin_request_text)
        await state.set_state(admin_states.request_admin)


@router.message(admin_states.request_admin)
async def request_admin(message: Message, state: FSMContext):
    if dbase.admin.has_auth_token(message.text):
        dbase.admin.delete_auth_token(message.text)
        dbase.admin.add_admin(message.chat.id)
        await message.answer(text="Поздравляю, теперь вы администратор")
        await state.set_state(start_states.none)


@router.callback_query(Text(admin_buttons.admin_panel.callback_data))
async def add_admin(callback: CallbackQuery, state: FSMContext):
    kb = InlineKeyboardBuilder()
    kb.row(admin_buttons.add_house)
    kb.row(admin_buttons.add_admin)
    await callback.message.edit_text(admin_texts.admin_panel,
                                     reply_markup=kb.as_markup())


@router.callback_query(Text(admin_buttons.add_admin.callback_data))
async def add_admin(callback: CallbackQuery, state: FSMContext):
    admin_token = randomword()
    dbase.admin.set_auth_token(admin_token)
    kb = InlineKeyboardBuilder()
    kb.row(admin_buttons.add_house)
    kb.row(admin_buttons.add_admin)
    await callback.message.edit_text(f"Вот токен для добавления нового администратора:{admin_token}\n"
                                                     f"Используйте команду /admin_request",
                                                     reply_markup=kb.as_markup())
