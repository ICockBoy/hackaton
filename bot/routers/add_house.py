import random
import string
from copy import deepcopy
from typing import Union

from aiogram import Router
from aiogram.filters import Command, Text, BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

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
        if isinstance(self.chat_type, str):
            return message.chat.type == self.chat_type
        else:
            return message.chat.type in self.chat_type


@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]))
async def write_house_name(message: Message, state: FSMContext):
    if dbase.admin.is_admin(message.from_user.id):
        kb = InlineKeyboardBuilder()
        kb.row(InlineKeyboardButton(text="Проверить", callback_data=f"check_group/{message.chat.id}"))
        await message.answer("Вы хотите использовать эту группу?", reply_markup=kb.as_markup())


groups = {

}


@router.callback_query(Text(startswith="check_group"))
async def add_house(callback: CallbackQuery, state: FSMContext):
    if dbase.admin.is_admin(callback.from_user.id):
        group_id = callback.data.split("/")[1]
        group = await bot.get_chat(group_id)
        if not group.is_forum:
            await callback.answer("Сделайте группу форумом")
        member = await bot.get_chat_member(callback.message.chat.id, token.split(":")[0])
        if member.status != "administrator":
            await callback.answer("Сделайте бота администратором")
        if not all([member.can_manage_chat, member.can_manage_topics]):
            await callback.answer("Дайте боту все привелегии")

