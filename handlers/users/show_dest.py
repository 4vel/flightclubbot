import logging
from aiogram import types
from aiogram.dispatcher.filters import Command
from db.models import TableUserAirports
from app import session, iata_name_dict
from loader import dp


def get_destinations_by_user(dbsession, user_id):
    """ Возвращает все направления и цены, указанные пользователем """

    user_id = str(user_id)
    destinations_dict = dict()
    for el in dbsession.query(TableUserAirports).filter_by(user_id = user_id).all():
        destinations_dict[el.airport_code] = int(el.price)
    return destinations_dict


@dp.message_handler(Command("show_destinations"))
async def show_destinations(message: types.Message):
    dst = get_destinations_by_user(session, message.from_user.id)
    if dst:
        msg = "У вас указаные следующие направления ...\n"
        for k, v in dst.items():
            msg += f"{k} {iata_name_dict.get(k)} - {v} ₽ \n"
    else:
        msg = """ У вас пока не указано ни одно направление"""
    await message.answer(msg)
