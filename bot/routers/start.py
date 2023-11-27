import asyncio
from typing import Union

from aiogram import Router
from aiogram.filters import Command, Text, BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.base import dbase, bot
from bot.states import start_states
from bot.texts import start as start_texts
from bot.buttons import start as start_buttons
from bot.texts import register as register_texts
from bot.buttons import admin as admin_buttons

router = Router()


class ChatTypeFilter1(BaseFilter):  # [1]
    def __init__(self, chat_type: Union[str, list]):  # [2]
        self.chat_type = chat_type

    async def __call__(self, message: Message) -> bool:
        if isinstance(self.chat_type, str):
            return not (message.chat.type == self.chat_type)
        else:
            return not (message.chat.type in self.chat_type)


@router.message(Command("start"), ChatTypeFilter1(chat_type=["group", "supergroup"]))
async def start_command(message: Message, state: FSMContext):
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
        return
    if not dbase.users_manager.user_in_database(message.chat.id):
        kb = InlineKeyboardBuilder()
        kb.row(start_buttons.register)
        kb.row(start_buttons.button_faq)
        await message.answer(start_texts.unregistered_user, reply_markup=kb.as_markup())
    elif dbase.users_manager.user_in_register(message.chat.id):
        await message.answer(register_texts.in_moderate)
    else:
        house = dbase.houses.get_house(dbase.houses.find_user_house(message.chat.id))
        group = await bot.get_chat(house.users_group_id)
        user = dbase.users_manager.get_user(message.chat.id)
        kb = InlineKeyboardBuilder()
        kb.row(InlineKeyboardButton(text="Чат жильцов", url=group.invite_link))
        kb.row(start_buttons.button_reports)
        kb.row(start_buttons.button_requests)
        kb.row(start_buttons.button_faq)
        kb.row(start_buttons.parking)
        kb.row(start_buttons.exit_from_account)
        await message.answer(start_texts.personal_menu.format(user.fio), reply_markup=kb.as_markup())


@router.callback_query(Text("start"))
async def start_callback(callback: CallbackQuery, state: FSMContext):
    if dbase.houses.find_user_house(callback.message.chat.id) is None:
        kb = InlineKeyboardBuilder()
        kb.row(start_buttons.button_faq)
        await callback.message.edit_text(start_texts.not_in_group_user, reply_markup=kb.as_markup())
        return
    if not dbase.users_manager.user_in_database(callback.message.chat.id):
        kb = InlineKeyboardBuilder()
        kb.row(start_buttons.register)
        kb.row(start_buttons.button_faq)
        await callback.message.edit_text(start_texts.unregistered_user, reply_markup=kb.as_markup())
    elif dbase.users_manager.user_in_register(callback.message.chat.id):
        await callback.message.edit_text(register_texts.in_moderate)
    else:
        house = dbase.houses.get_house(dbase.houses.find_user_house(callback.message.chat.id))
        group = await bot.get_chat(house.users_group_id)
        user = dbase.users_manager.get_user(callback.message.chat.id)
        kb = InlineKeyboardBuilder()
        kb.row(InlineKeyboardButton(text="Чат жильцов", url=group.invite_link))
        kb.row(start_buttons.button_reports)
        kb.row(start_buttons.button_requests)
        kb.row(start_buttons.button_faq)
        kb.row(start_buttons.parking)
        kb.row(start_buttons.exit_from_account)
        await callback.message.edit_text(start_texts.personal_menu.format(user.fio), reply_markup=kb.as_markup())


@router.callback_query(Text(start_buttons.user_to_house.callback_data))
async def user_to_house(callback: CallbackQuery, state: FSMContext):
    if dbase.houses.find_user_house(callback.from_user.id) is not None:
        await callback.answer("Вы уже закреплены за другим домом")
    else:
        house_name = dbase.houses.find_house_from_group_id(callback.message.chat.id)
        dbase.houses.add_user(house_name, callback.from_user.id)
        await callback.answer("Успешно!✅ Вы закреплены за домом. Теперь можете перейти в бота.", show_alert=True)


@router.callback_query(Text(start_buttons.exit_from_account.callback_data))
async def exit_from_account(callback: CallbackQuery, state: FSMContext):
    kb = InlineKeyboardBuilder()
    kb.row(start_buttons.decline_exit, start_buttons.accept_exit)
    await callback.message.edit_text(start_texts.exit_confirm, reply_markup=kb.as_markup())


@router.callback_query(Text(start_buttons.accept_exit.callback_data))
async def accept_exit(callback: CallbackQuery, state: FSMContext):
    dbase.users_manager.remove_user(callback.message.chat.id)
    await callback.message.edit_text(start_texts.exit_success)


class ChatTypeFilter2(BaseFilter):  # [1]
    def __init__(self, chat_type: Union[str, list]): # [2]
        self.chat_type = chat_type

    async def __call__(self, message: Message) -> bool:
        if not dbase.admin.is_admin(message.from_user.id) and message.text is not None:
            if isinstance(self.chat_type, str):
                return message.chat.type == self.chat_type
            else:
                return message.chat.type in self.chat_type


@router.message(ChatTypeFilter2(chat_type=["group", "supergroup"]))
async def start_command(message: Message, state: FSMContext):
    if not dbase.users_manager.user_in_database(message.from_user.id):
        message_new = await message.reply("Авторизуйтесь в боте, чтобы писать в эту группу")
        await message.delete()
        await asyncio.sleep(5)
        await message_new.delete()
        return
    user = dbase.users_manager.get_user(message.from_user.id)
    await message.reply(f"ФИО: {user.fio}\nподъезд: {user.entrance}\nэтаж: {user.floor}\nквартира: {user.apartment}\nномер телефона: {user.number}")