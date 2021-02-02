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
    msg = f"""
    Привет, {message.from_user.first_name}! Хочешь улететь? ✈️ 
    FlightClubber поможет тебе найти авиабилеты по цене ниже той, которую ты укажешь.
    Просто укажи город или аэропорт вылета и добавь направление и пороговое значение цены. 
    Как только FlightClubber найдет билет дешевле, ты сразу получишь сообщение.
    """
    await message.answer(msg)
    # await message.answer(f'Твой user_id {message.from_user.id}')
    await message.answer(f'Укажи код аэропорта отправления')
    await FormBaseAeroport.Q1.set()


@dp.message_handler(state=FormBaseAeroport.Q1)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text.upper()
    if iata_name_dict.get(answer):
        await state.update_data(answer1=answer)
        await message.answer(f"Аэропорт отправления записан - {answer} {iata_name_dict.get(answer)}")

        user_id = str(message.from_user.id)
        session.query(TableUsers).filter_by(user_id = user_id).delete()

        meuser = TableUsers(user_id, message.from_user.full_name, answer)
        session.add(meuser)
        session.commit()
        await message.answer(f"Теперь можешь добавить город для отслеживания цен на авиабилеты 👉/add_destination_city")
        await state.reset_state()
    else:
        await message.answer(f'Такого кода аэропорта нет.')
        await state.reset_state()

