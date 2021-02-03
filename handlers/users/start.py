import logging
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from db.models import TableUserAirports, TableUsers
from db.utils import add_airport_origin
from states.form import FormBaseAeroport
from app import session, iata_name_dict
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    msg = f"Привет, {message.from_user.first_name}! Хочешь улететь? ✈️ " \
          "FlightClubber поможет тебе найти авиабилеты по цене ниже той, которую ты укажешь. " \
          "Просто укажи город или аэропорт вылета и добавь направление и пороговое значение цены. " \
          "Как только FlightClubber найдет билет дешевле, ты сразу получишь сообщение."
    await message.answer(msg)
    # await message.answer(f'Твой user_id {message.from_user.id}')
    await message.answer(f'Для начала укажи код аэропорта отправления')
    await FormBaseAeroport.Q1.set()


@dp.message_handler(state=FormBaseAeroport.Q1)
async def answer_q1(message: types.Message, state: FSMContext):
    airport_origin = message.text.upper()
    if iata_name_dict.get(airport_origin):

        await state.update_data(answer1=airport_origin)
        await message.answer(f"Аэропорт отправления записан - {airport_origin} {iata_name_dict.get(airport_origin)}")
        user_id = str(message.from_user.id)
        user_fullname = str(message.from_user.full_name)
        add_airport_origin(session, user_id, user_fullname, airport_origin)



        await message.answer(f"Теперь можешь добавить город для отслеживания цен на авиабилеты 👉/add_destination_city")
        await state.reset_state()

    else:
        await message.answer(f'Такого кода аэропорта нет.')
        await state.reset_state()
