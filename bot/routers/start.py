from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.base import dbase, bot
from bot.config import moderate_channel
from bot.states import start_states
from bot.texts import start as start_texts
from bot.buttons import start as start_buttons
from bot.texts import register as register_texts
from bot.buttons import admin as admin_buttons


router = Router()


@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    print(await state.get_data())
    if dbase.admin.is_admin(message.chat.id):
        kb = InlineKeyboardBuilder()
        kb.row(admin_buttons.admin_panel)
        kb.row(start_buttons.user_menu)
        await message.answer(start_texts.choose_menu, reply_markup=kb.as_markup())
        await state.set_state(start_states.none)
        return
    if dbase.houses.find_user_house(message.chat.id) is None:
        kb = InlineKeyboardBuilder()
        kb.row(start_buttons.button_faq)
        await message.answer(start_texts.not_in_group_user, reply_markup=kb.as_markup())
    if not dbase.users_manager.user_in_database(message.chat.id):
        kb = InlineKeyboardBuilder()
        kb.row(start_buttons.register)
        kb.row(start_buttons.button_faq)
        await message.answer(start_texts.unregistered_user, reply_markup=kb.as_markup())
    elif dbase.users_manager.user_in_register(message.chat.id):
        await message.answer(register_texts.in_moderate)
    else:
        user = dbase.users_manager.get_user(message.chat.id)
        kb = InlineKeyboardBuilder()
        kb.row(start_buttons.button_member_chats)
        kb.row(start_buttons.button_reports)
        kb.row(start_buttons.button_requests)
        kb.row(start_buttons.button_faq)
        kb.row(start_buttons.exit_from_account)
        await message.answer(start_texts.personal_menu.format(user.fio), reply_markup=kb.as_markup())


@router.callback_query(Text("start"))
async def start_callback(callback: CallbackQuery, state: FSMContext):
    if not dbase.users_manager.user_in_database(callback.message.chat.id):
        kb = InlineKeyboardBuilder()
        kb.row(start_buttons.register)
        kb.row(start_buttons.button_faq)
        await callback.message.edit_text(start_texts.unregistered_user, reply_markup=kb.as_markup())
    elif dbase.users_manager.user_in_register(callback.message.chat.id):
        await callback.message.edit_text(register_texts.in_moderate)
    else:
        user = dbase.users_manager.get_user(callback.message.chat.id)
        kb = InlineKeyboardBuilder()
        kb.row(start_buttons.button_member_chats)
        kb.row(start_buttons.button_reports)
        kb.row(start_buttons.button_requests)
        kb.row(start_buttons.button_faq)
        kb.row(start_buttons.exit_from_account)
        await callback.message.edit_text(start_texts.personal_menu.format(user.fio), reply_markup=kb.as_markup())


@router.callback_query(Text(start_buttons.exit_from_account.callback_data))
async def exit_from_account(callback: CallbackQuery, state: FSMContext):
    kb = InlineKeyboardBuilder()
    kb.row(start_buttons.decline_exit, start_buttons.accept_exit)
    await callback.message.edit_text(start_texts.exit_confirm, reply_markup=kb.as_markup())


@router.callback_query(Text(start_buttons.accept_exit.callback_data))
async def accept_exit(callback: CallbackQuery, state: FSMContext):
    dbase.users_manager.remove_user(callback.message.chat.id)
    await callback.message.edit_text(start_texts.exit_success)
