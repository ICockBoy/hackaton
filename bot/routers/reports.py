import asyncio
import re
from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.base import dbase, bot
from bot.states import register_states, start_states, reports_states
from bot.subjects.user import User
from bot.texts import reports as reports_texts
from bot.buttons import start as start_buttons
from bot.buttons import reports as reports_buttons

router = Router()


@router.callback_query(Text(start_buttons.button_reports.callback_data))
async def button_reports(callback: CallbackQuery, state: FSMContext):
    kb = InlineKeyboardBuilder()
    kb.row(reports_buttons.choose1)
    kb.row(reports_buttons.choose2)
    kb.row(reports_buttons.choose3)
    kb.row(reports_buttons.choose4)
    await callback.message.edit_text(reports_texts.problem_choose, reply_markup=kb.as_markup())


@router.callback_query(Text(reports_buttons.choose1.callback_data))
@router.callback_query(Text(reports_buttons.choose2.callback_data))
@router.callback_query(Text(reports_buttons.choose3.callback_data))
@router.callback_query(Text(reports_buttons.choose4.callback_data))
async def button_reports(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    print(callback.data)
    await callback.message.edit_text(reports_texts.problem_write_text)
    if callback.data == reports_buttons.choose1.callback_data:
        data["problem_type"] = reports_buttons.choose1.text
    if callback.data == reports_buttons.choose2.callback_data:
        data["problem_type"] = reports_buttons.choose2.text
    if callback.data == reports_buttons.choose3.callback_data:
        data["problem_type"] = reports_buttons.choose3.text
    if callback.data == reports_buttons.choose4.callback_data:
        data["problem_type"] = reports_buttons.choose4.text
    await state.set_data(data)
    await state.set_state(reports_states.write_problem)


@router.message(reports_states.write_problem)
async def write_problem(message: Message, state: FSMContext):
    data = await state.get_data()
    text = reports_texts.problem_text.format(data["problem_type"], message.text)
    kb = InlineKeyboardBuilder()
    kb.row(reports_buttons.report_retry)
    kb.row(reports_buttons.report_accept)
    await message.answer(text, reply_markup=kb.as_markup())


@router.callback_query(Text(reports_buttons.report_accept.callback_data))
async def report_accept(callback: CallbackQuery, state: FSMContext):
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="Проблема решена", callback_data=f"problem_accept/{callback.from_user.id}"))
    kb.row(
        InlineKeyboardButton(text="Написать пользователю", url=f"https://t.me/{callback.from_user.username}"))
    house_name = dbase.houses.find_user_house(callback.message.chat.id)
    house = dbase.houses.get_house(house_name)
    await bot.send_message(house.moderate_group_id,
                           callback.message.text,
                           message_thread_id=house.moderate_topic_reports,
                           reply_markup=kb.as_markup())
    await callback.message.edit_text(reports_texts.problem_to_moderate)
    await state.set_state(start_states.none)


@router.callback_query(Text(startswith="problem_accept"))
async def problem_accept(callback: CallbackQuery, state: FSMContext):
    user_id = callback.data.split("/")[1]
    await bot.send_message(user_id, reports_texts.problem_is_not_problem + "\n\n" + callback.message.text)
    await callback.message.edit_text("Успешно!✅")
    await asyncio.sleep(5)
    await callback.message.delete()
