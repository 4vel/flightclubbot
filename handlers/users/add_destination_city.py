import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from db.utils import add_destination, check_existing_destination, remove_existing_destination
from loader import dp
from states.destination import DestinationCity
from app import session, iata_name_dict, city_code_lists
from sqlalchemy.exc import SQLAlchemyError


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
    city_name = data.get("answer1")
    city_name_low = city_name.lower()
    price = data.get("answer2")
    user = str(message.from_user.id)
    logging.info(f"{city_name} {price} {user}")

    # проверяем есть ли код в списке аэропортов
    if city_code_lists.get(city_name_low):
        list_of_codes = city_code_lists.get(city_name_low)
        if len(list_of_codes) == 1:
            try:
                city_code = city_code_lists.get(city_name_low)[0]
                if check_existing_destination(session, user, city_code):
                    remove_existing_destination(session, user, city_code)
                add_destination(session, user, city_code, price)

                await message.answer("Добавили в список!")
                await message.answer(f"Город - {city_name} {city_code}")
                await message.answer(f"Цена - {price} ₽")
                await message.answer(f"Еще город? 👉 /add_destination_city")
                await state.reset_state()

            except SQLAlchemyError as e:
                logging.info(f'SQLAlchemyError {e}')
                await message.answer("Кажется, что-то пошло не так. Попробуйте еще раз немного позже.")
                await state.reset_state()
        else:
            await message.answer("В списке IATA кодов городов с таким названием больше одного")
            msg = "Попробуй выбрать из списка правильный код и затем добавить его командой /add_destination "
            await message.answer(msg)
            for x in list_of_codes:
                msg = x + ' ' + iata_name_dict.get(x)
                await message.answer(msg)
            await state.reset_state()

    else:
        await message.answer("К сожалению, такого города у нас еще нет в списке")
        await state.reset_state()




