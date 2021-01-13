from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dphttps://github.com/4vel/flightclubbot.git
from utils.misc import rate_limit


@rate_limit(5, 'help')
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = [
        """
         Это бот FlightClubber✈️. Он самостоятельно проверяет цены на авиабилеты сравнивая их
         с заданными пороговыми значениями. При появлении более низких цен, отправляет сообщение в телеграм """,
        'Список команд: ',
        '/start - Начать диалог и указать аэропорт отправления',
        '/help - Получить справку',
        '/add_destination - Добавить код аэропорта и цену для поиска билетов',
        '/show_destinations - Показать список указанных аэропортов и цен',
        '/remove_destinations - Удалить все направления из списка ',
    ]
    await message.answer('\n'.join(text))
