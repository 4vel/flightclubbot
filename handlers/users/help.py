from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp
from utils.misc import rate_limit


@rate_limit(5, 'help')
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    intro_msg = "FlightClubber✈️ самостоятельно проверяет цены на авиабилеты, сравнивая их "\
                "с заданными пороговыми значениями. При появлении более низких цен, отправляет сообщение в телеграм "
    text = [
        intro_msg,
        'Список команд: ',
        '/start - Начать диалог и указать аэропорт отправления 🚀',
        '/help - Получить справку 🆘',
        '/add_destination - Добавить направление по коду аэропорта или города для поиска билетов 🌏',
        '/add_destination_city - Добавить направление по названию города для поиска билетов 🌎',
        '/show_destinations - Показать список указанных направлений и пороговых значений цен ✅',
        '/remove_destinations - Удалить все направления из списка ❌',
    ]
    await message.answer('\n'.join(text))
