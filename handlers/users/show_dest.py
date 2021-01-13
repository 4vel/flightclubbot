import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from db.models import TableUserAirports

from config import conn_string
from loader import dp
from states.form import Form

session = dal.get_session()

def get_destinations_by_user():
    pass
    return None

@dp.message_handler(Command("show_destinations"))
async def enter_form(message: types.Message):

    dst = get_destinations_by_user()
    if dst:
        msg = """У вас указаные следующие направления ..."""
        msg = msg + dst
    else:
        msg = """ У вас пока не указано ни одно направление"""
    await message.answer(msg)



