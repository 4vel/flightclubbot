from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("help", "Помощь"),
        types.BotCommand("add_destination", "Добавить направление"),
        types.BotCommand("add_destination_city", "Добавить город "),
        types.BotCommand("show_destinations", "Посмотреть направления"),
        types.BotCommand("remove_destinations", "Удалить все направления"),
    ])
