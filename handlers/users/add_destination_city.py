import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from db.models import TableUserAirports, TableCities
from db.utils import add_destination, check_existing_destination, remove_existing_destination
from loader import dp
from states.destination import DestinationCity
from app import session, iata_name_dict, city_code_lists


@dp.message_handler(Command("add_destination_city"))
async def enter_form_city(message: types.Message):
    msg = """
    Укажите направление для отслеживания цен на авиабилеты
    """

    await message.answer(msg)
    await message.answer("Укажите город \n")
    await DestinationCity.Q1.set()
    # проверяем есть ли город в списке
    # проверяем сколько стран с таким городом
    # если стран несколько, то предлагаем уточнить страну


@dp.message_handler(state=DestinationCity.Q1)
async def answer_q1_city(message: types.Message, state: FSMContext):
    answer = message.text

    await state.update_data(answer1=answer)
    await message.answer("Укажите максимальный порог цены в рублях \n")
    await DestinationCity.next()

@dp.message_handler(state=DestinationCity.Q2)
async def answer_q2_city(message: types.Message, state: FSMContext):

    answer = message.text
    await state.update_data(answer2 = answer)

    data = await state.get_data()
    city_code = data.get("answer1")
    price = data.get("answer2")

    # проверяем есть ли код в списке аэропортов
    # if iata_name_dict.get(city_code.upper()):

    user = str(message.from_user.id)
    logging.info(f"{city_code} {price} {user}")

    # if check_existing_destination(session, user, city_code):
    #     remove_existing_destination(session, user, city_code)
    # add_destination(session, user, city_code, price)

    await message.answer("Добавили в список!")
    await message.answer(f"Город - {city_code} {city_code_lists.get(city_code)}")
    await message.answer(f"Цена - {price} р")
    await state.reset_state()

    # else:
    #     await message.answer("К сожалению, такого города у нас еще нет")
    #     await state.reset_state()