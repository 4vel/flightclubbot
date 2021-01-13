import logging
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from db.models import TableUserAirports, TableUsers
from states.form import FormBaseAeroport
from app import session, iata_name_dict
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.full_name}!')
    # await message.answer(f'Твой user_id {message.from_user.id}')
    await message.answer(f'Укажи код аэропорта отправления')
    await FormBaseAeroport.Q1.set()


@dp.message_handler(state=FormBaseAeroport.Q1)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    if iata_name_dict.get(answer):
        await state.update_data(answer1=answer)
        await message.answer(f"Аэропорт отправления записан - {answer} {iata_name_dict.get(answer)}")

        meuser = TableUsers(message.from_user.id, message.from_user.full_name, answer)
        session.add(meuser)
        session.commit()
        await state.reset_state()
    else:
        await message.answer(f'Такого кода аэропорта нет.')
        await state.reset_state()

