import logging
import pickle
import os
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from db.models import TableUserAirports
# from db.models import DataAccessLayer
# from config import conn_string
from config import IATA_PKL_PATH
from loader import dp
from states.form import Form
from app import session

with open(IATA_PKL_PATH, 'rb') as f:
    iata_name_dict = pickle.load(f)


# dal = DataAccessLayer(conn_string)
# session = dal.get_session()

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
    answer1 = data.get("answer1")
    answer2 = data.get("answer2")

    # проверяем есть ли код в списке аэропортов
    if iata_name_dict.get(answer1):
        user = str(message.from_user.id)
        logging.info(f"{answer1}{answer2} {user}")
        uap = TableUserAirports(user, answer1, int(answer2))
        session.add(uap)
        session.commit()

        await message.answer("Добавили в список !")
        await message.answer(f"Аэропорт - {answer1} {iata_name_dict.get(answer1)}")
        await message.answer(f"Цена - {answer2}")
        await state.reset_state()

    else:
        await message.answer("К сожалению, такого кода аэропорта у нас еще нет")