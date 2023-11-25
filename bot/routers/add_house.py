import asyncio
import random
import string
from copy import deepcopy
from typing import Union

from aiogram import Router
from aiogram.filters import Command, Text, BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, ChatPermissions
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.buttons import start as start_buttons

from bot.config import token
from bot.subjects.house import House
from bot.texts import add_house as add_house_texts
from bot.buttons import admin as admin_buttons
from bot.buttons import add_house as add_house_buttons

from bot.states import admin_states, start_states, add_house_states

from bot.base import dbase, bot, dp, memory_storage

router = Router()


@router.callback_query(Text(admin_buttons.add_house.callback_data))
async def add_house(callback: CallbackQuery, state: FSMContext):
    kb = InlineKeyboardBuilder()
    kb.row(admin_buttons.back)
    await callback.message.edit_text(add_house_texts.write_house_name,
                                     reply_markup=kb.as_markup())
    await state.set_state(add_house_states.write_house_name)


@router.message(add_house_states.write_house_name)
async def write_house_name(message: Message, state: FSMContext):
    data = await state.get_data()
    data["house_name"] = message.text
    await state.set_data(data)
    kb = InlineKeyboardBuilder()
    kb.row(admin_buttons.back)
    await message.answer(add_house_texts.get_users_group.format(),
                         reply_markup=kb.as_markup())
    await state.set_state(add_house_states.get_users_group)


class ChatTypeFilter(BaseFilter):  # [1]
    def __init__(self, chat_type: Union[str, list]): # [2]
        self.chat_type = chat_type

    async def __call__(self, message: Message) -> bool:
        state: FSMContext = dp.fsm.resolve_context(bot, message.from_user.id, message.from_user.id)
        if ((await state.get_state()) == add_house_states.get_moderate_group or (await state.get_state()) == add_house_states.get_users_group) and dbase.admin.is_admin(message.from_user.id):
            if isinstance(self.chat_type, str):
                return message.chat.type == self.chat_type
            else:
                return message.chat.type in self.chat_type


@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]))
async def write_house_name(message: Message):
    state: FSMContext = dp.fsm.resolve_context(bot, message.from_user.id, message.from_user.id)
    data = await state.get_data()
    if f"message_in_chat{message.chat.id}" not in data:
        data[f"message_in_chat{message.chat.id}"] = True
        await state.set_data(data)
        kb = InlineKeyboardBuilder()
        kb.row(InlineKeyboardButton(text="Проверить", callback_data=f"check_group/{message.chat.id}"))
        await message.answer("Вы хотите использовать эту группу?", reply_markup=kb.as_markup())


@router.callback_query(Text(startswith="check_group"))
async def add_house(callback: CallbackQuery):
    state: FSMContext = dp.fsm.resolve_context(bot, callback.from_user.id, callback.from_user.id)
    group_id = callback.data.split("/")[1]
    group = await bot.get_chat(group_id)
    if not group.is_forum:
        await callback.answer("Сделайте группу форумом")
        return
    member = await bot.get_chat_member(callback.message.chat.id, token.split(":")[0])
    if member.status != "administrator":
        await callback.answer("Сделайте бота администратором")
        return
    if not all([member.can_manage_chat, member.can_manage_topics]):
        await callback.answer("Дайте боту все привелегии")
        return
    data = await state.get_data()

    if await state.get_state() == add_house_states.get_users_group:
        data["users_group_id"] = int(group_id)
        await state.set_data(data)
        kb = InlineKeyboardBuilder()
        kb.row(admin_buttons.back)
        await bot.send_message(callback.from_user.id, add_house_texts.get_moderate_group, reply_markup=kb.as_markup())
        await state.set_state(add_house_states.get_moderate_group)
        kb = InlineKeyboardBuilder()
        kb.row(start_buttons.user_to_house)
        kb.row(start_buttons.go_to_bot)
        await callback.message.edit_text(add_house_texts.reg_in_house, reply_markup=kb.as_markup())
        await callback.message.pin()
        chat_permissions = ChatPermissions()
        chat_permissions.can_send_messages = True
        chat_permissions.can_manage_topics = False
        chat_permissions.can_add_web_page_previews = False
        chat_permissions.can_change_info = False
        chat_permissions.can_invite_users = False
        chat_permissions.can_pin_messages = False
        chat_permissions.can_send_other_messages = False
        await bot.set_chat_title(group_id, data["house_name"])
        await bot.set_chat_permissions(group_id, chat_permissions)

    if await state.get_state() == add_house_states.get_moderate_group and data["users_group_id"] != int(group_id):
        data = await state.get_data()
        data["moderate_group_id"] = int(group_id)
        moderate_topic_register = await bot.create_forum_topic(group_id, "Регистрации")
        data["moderate_topic_register"] = moderate_topic_register.message_thread_id
        moderate_topic_reports = await bot.create_forum_topic(group_id, "Жалобы")
        data["moderate_topic_reports"] = moderate_topic_reports.message_thread_id
        moderate_topic_reports = await bot.create_forum_topic(group_id, "Запросы")
        data["moderate_topic_requests"] = moderate_topic_reports.message_thread_id
        house = House()
        house.users_group_id = data["users_group_id"]
        house.moderate_group_id = data["moderate_group_id"]
        house.moderate_topic_reports = data["moderate_topic_reports"]
        house.moderate_topic_requests = data["moderate_topic_requests"]
        house.moderate_topic_register = data["moderate_topic_register"]
        dbase.houses.set_house(data["house_name"], house)
        await state.set_data(data)
        kb = InlineKeyboardBuilder()
        kb.row(admin_buttons.add_house)
        kb.row(admin_buttons.add_admin)
        await bot.send_message(callback.from_user.id, add_house_texts.success_add_house, reply_markup=kb.as_markup())
        await state.set_state(start_states.none)
        await callback.message.edit_text("Успешно!✅")
        await asyncio.sleep(5)
        await callback.message.delete()

