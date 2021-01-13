import logging
from aiogram import types
from aiogram.dispatcher.filters import Command
from db.models import TableUserAirports
from app import session
from loader import dp



@dp.message_handler(Command("remove_destinations"))
async def remove_destinations(message: types.Message):

    user_id = str(message.from_user.id)
    session.query(TableUserAirports).filter_by(user_id=user_id).delete()
    session.commit()
    msg = """ Все ранее указанные аэропорты удалены"""
    logging.info(user_id)
    logging.info(msg)
    await message.answer(msg)
