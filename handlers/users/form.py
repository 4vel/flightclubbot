import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from db.models import TableUserAirports
from db.utils import add_destination, check_existing_destination, remove_existing_destination
from loader import dp
from states.form import Form
from app import session, iata_name_dict


@dp.message_handler(Command("add_destination"))
async def enter_form(message: types.Message):
    msg = """
    Укажите направление для отслеживания цен на авиабилеты
    """

    await message.answer(msg)
    await message.answer("Укажите IATA код аэропорта \n")
    await Form.Q1.set()



@dp.message_handler(state=Form.Q1)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text

    await state.update_data(answer1=answer)
    await message.answer("Укажите максимальный порог цены в рублях \n")
    await Form.next()

@dp.message_handler(state=Form.Q2)
async def answer_q2(message: types.Message, state: FSMContext):

    answer = message.text
    await state.update_data(answer2 = answer)

    data = await state.get_data()
    airport = data.get("answer1")
    answer2 = data.get("answer2")

    # проверяем есть ли код в списке аэропортов
    if iata_name_dict.get(airport.upper()):
        airport = airport.upper()
        user = str(message.from_user.id)
        logging.info(f"{airport}{answer2} {user}")
        # добавить функцию проверки этого направления
        # добавить функцию удаления если такое направление уже есть
        # добавить функцию добавления направления
        if check_existing_destination(session, user, airport):
            remove_existing_destination(session, user, airport)
        add_destination(session, user, airport, answer2)

        # uap = TableUserAirports(user, airport, int(answer2))
        # session.add(uap)
        # session.commit()

        await message.answer("Добавили в список !")
        await message.answer(f"Аэропорт - {airport} {iata_name_dict.get(airport)}")
        await message.answer(f"Цена - {answer2} ₽")
        await state.reset_state()

    else:
        await message.answer("К сожалению, такого кода аэропорта у нас еще нет")
        await state.reset_state()