import pickle
from utils.set_bot_commands import set_default_commands
from config import conn_string, IATA_PKL_PATH
from db.models import DataAccessLayer

with open(IATA_PKL_PATH, 'rb') as f:
    iata_name_dict = pickle.load(f)

dal = DataAccessLayer(conn_string)
session = dal.get_session()

async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    await set_default_commands(dp)


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
