import asyncio
import re
from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.base import dbase, bot
from bot.states import requests_states, start_states
from bot.subjects.user import User
from bot.texts import requests as requests_texts
from bot.buttons import start as start_buttons
from bot.buttons import requests as requests_buttons

router = Router()


@router.callback_query(Text(start_buttons.button_requests.callback_data))
async def button_reports(callback: CallbackQuery, state: FSMContext):
    kb = InlineKeyboardBuilder()
    kb.row(requests_buttons.back)
    await callback.message.edit_text(requests_texts.send_your_request, reply_markup=kb.as_markup())
    await state.set_state(requests_states.write_request)


@router.message(requests_states.write_request)
async def write_request(message: Message, state: FSMContext):
    if message.text is None:
        await message.answer("Нужно писать заявки исключительно текстом")
        return
    kb = InlineKeyboardBuilder()
    kb.row(requests_buttons.request_retry)
    kb.row(requests_buttons.request_accept)
    await message.answer(requests_texts.request_text.format(message.text), reply_markup=kb.as_markup())


@router.callback_query(Text(requests_buttons.request_accept.callback_data))
async def request_accept(callback: CallbackQuery, state: FSMContext):
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="На всеобщее обсуждение", callback_data=f"request_to_all/{callback.from_user.id}"))
    kb.row(InlineKeyboardButton(text="Заявка обработана", callback_data=f"request_to_user/{callback.from_user.id}"))
    kb.row(
        InlineKeyboardButton(text="Написать пользователю", url=f"https://t.me/{callback.from_user.username}"))
    house_name = dbase.houses.find_user_house(callback.message.chat.id)
    house = dbase.houses.get_house(house_name)
    user = dbase.users_manager.get_user(callback.message.chat.id)
    await bot.send_message(house.moderate_group_id,
                           callback.message.text + f"\n\n->ФИО: {user.fio}\nподъезд: {user.entrance}\nэтаж: {user.floor}\nквартира: {user.apartment}\nномер телефона: {user.number}",
                           message_thread_id=house.moderate_topic_requests,
                           reply_markup=kb.as_markup())
    await callback.message.edit_text(requests_texts.request_was_send)
    await state.set_state(start_states.none)


@router.callback_query(Text(startswith="request_to_user"))
async def request_to_user(callback: CallbackQuery, state: FSMContext):
    user_id = callback.data.split("/")[1]
    await bot.send_message(user_id, requests_texts.request_was_approved + "\n\n" + callback.message.text)
    await callback.message.edit_text("Успешно!✅")
    await asyncio.sleep(5)
    await callback.message.delete()


@router.callback_query(Text(startswith="request_to_all"))
async def request_to_user(callback: CallbackQuery, state: FSMContext):
    user_id = callback.data.split("/")[1]
    house_name = dbase.houses.find_user_house(user_id)
    house = dbase.houses.get_house(house_name)
    if "Предложения" not in house.users_group_topics:
        topic = await bot.create_forum_topic(house.users_group_id, "Предложения")
        house.users_group_topics["Предложения"] = topic.message_thread_id
        dbase.houses.set_house(house_name, house)
    await bot.send_message(house.users_group_id,
                           callback.message.text + "\nГолосуйте за предложение эможди (лайки, дизлайки)",
                           message_thread_id=house.users_group_topics["Предложения"])
    await bot.send_message(user_id, requests_texts.request_was_approved_to_all + "\n\n" + callback.message.text)
    await callback.message.edit_text("Успешно!✅")
    await asyncio.sleep(5)
    await callback.message.delete()
