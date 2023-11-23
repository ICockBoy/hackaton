import asyncio
import re
from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.base import dbase, bot
from bot.config import moderate_channel
from bot.states import register_states, start_states
from bot.subjects.user import User
from bot.texts import register as register_texts
from bot.buttons import start as start_buttons
from bot.buttons import register as register_buttons

router = Router()


@router.callback_query(Text(start_buttons.register.callback_data))
async def register_fio(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(register_texts.write_fio)
    await state.set_state(register_states.fio_send)


@router.message(register_states.fio_send)
async def fio_send(message: Message, state: FSMContext):
    if any(map(str.isdigit, message.text)):
        await message.answer(register_texts.incorrect_data)
        return
    data = await state.get_data()
    data["fio"] = message.text
    await state.set_data(data)
    await message.answer(register_texts.write_entrance.format(data["fio"]))
    await state.set_state(register_states.entrance_send)


@router.message(register_states.entrance_send)
async def entrance_send(message: Message, state: FSMContext):
    if not message.text.isnumeric():
        await message.answer(register_texts.incorrect_data)
        return
    data = await state.get_data()
    data["entrance"] = message.text
    await state.set_data(data)
    await message.answer(register_texts.write_floor.format(data["fio"], data["entrance"]))
    await state.set_state(register_states.floor_send)


@router.message(register_states.floor_send)
async def floor_send(message: Message, state: FSMContext):
    if not message.text.isnumeric():
        await message.answer(register_texts.incorrect_data)
        return
    data = await state.get_data()
    data["floor"] = message.text
    await state.set_data(data)
    await message.answer(register_texts.write_apartment.format(data["fio"], data["entrance"], data["floor"]))
    await state.set_state(register_states.apartment_send)


@router.message(register_states.apartment_send)
async def apartment_send(message: Message, state: FSMContext):
    if not message.text.isnumeric():
        await message.answer(register_texts.incorrect_data)
        return
    data = await state.get_data()
    data["apartment"] = message.text
    await state.set_data(data)
    await message.answer(register_texts.write_number.format(data["fio"],
                                                            data["entrance"],
                                                            data["floor"],
                                                            data["apartment"]))
    await state.set_state(register_states.number_send)


@router.message(register_states.number_send)
async def number_send(message: Message, state: FSMContext):
    if not re.match(r'^8\d{10}$', message.text.replace(" ", "")):
        await message.answer(register_texts.incorrect_data)
        return
    data = await state.get_data()
    data["number"] = message.text
    await state.set_data(data)
    kb = InlineKeyboardBuilder()
    kb.row(register_buttons.retry_register)
    kb.row(register_buttons.all_good)
    await message.answer(register_texts.check_your_data.format(data["fio"],
                                                               data["entrance"],
                                                               data["floor"],
                                                               data["apartment"],
                                                               data["number"]),
                         reply_markup=kb.as_markup())
    await state.set_state(start_states.none)


@router.callback_query(Text(register_buttons.all_good.callback_data))
async def all_good(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user = User()
    user.fio = data["fio"]
    user.entrance = data["entrance"]
    user.floor = data["floor"]
    user.apartment = data["apartment"]
    user.number = data["number"]
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="Одобрить", callback_data=f"accept_order/{callback.message.chat.id}"))
    kb.row(InlineKeyboardButton(text="Отклонить", callback_data=f"decline_order/{callback.message.chat.id}"))
    dbase.users_manager.save_user(callback.message.chat.id, user)
    await bot.send_message(moderate_channel,
                           register_texts.in_moderate_to_admin.format(data["fio"],
                                                                      data["entrance"],
                                                                      data["floor"],
                                                                      data["apartment"],
                                                                      data["number"]),
                           reply_markup=kb.as_markup())
    await callback.message.edit_text(register_texts.in_moderate)
    await state.set_state(start_states.none)


@router.callback_query(Text(startswith="accept_order"))
async def accept_order(callback: CallbackQuery, state: FSMContext):
    user_id = callback.data.split("/")[1]
    user = dbase.users_manager.get_user(user_id)
    user.in_register = False
    dbase.users_manager.save_user(user_id, user)
    await bot.send_message(int(user_id), register_texts.request_was_approved)
    await callback.message.edit_text(register_texts.success)
    await asyncio.sleep(5)
    await callback.message.delete()


@router.callback_query(Text(startswith="decline_order"))
async def accept_order(callback: CallbackQuery, state: FSMContext):
    user_id = callback.data.split("/")[1]
    dbase.users_manager.remove_user(user_id)
    await bot.send_message(int(user_id), register_texts.request_was_declined)
    await callback.message.edit_text(register_texts.success)
    await asyncio.sleep(5)
    await callback.message.delete()
