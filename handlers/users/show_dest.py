import logging
from aiogram import types
from aiogram.dispatcher.filters import Command
from db.utils import get_destinations_by_user
from app import session, iata_name_dict
from loader import dp



@dp.message_handler(Command("show_destinations"))
async def show_destinations(message: types.Message):
    dst = get_destinations_by_user(session, message.from_user.id)
    if dst:
        msg = "Ты хочешь полететь сюда 👇\n"
        for k, v in dst.items():
            msg += f"{k} {iata_name_dict.get(k)} - {v} ₽ \n"
    else:
        msg = "У тебя пока не указано ни одно направление. " \
              "Это можно исправить с помощью команды 👉 /add_destination_city"
    await message.answer(msg)

