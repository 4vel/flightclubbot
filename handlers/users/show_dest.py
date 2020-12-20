import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from db.models import TableUserAirports

from config import conn_string
from loader import dp
from states.form import Form

session = dal.get_session()

@dp.message_handler(Command("add_destination"))
async def enter_form(message: types.Message):
    msg = """
    Укажите направление для отслеживания цен на авиабилеты
    """
    await message.answer(msg)
    await message.answer("Укажите IATA код аэропорта \n")
    await Form.Q1.set()
