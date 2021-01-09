import os
from dotenv import load_dotenv

load_dotenv()

DATAFILE_PATH = os.path.join('FlightDeals.xlsx')
TEQUILA_API_KEY = str(os.getenv("TEQUILA_API_KEY"))
BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
ADMIN_ID = int(os.getenv("ADMIN_ID"))
admins = [
    ADMIN_ID
]

# DB
DATABASE_USER = str(os.getenv("DBUSER"))
DATABASE_PASS = str(os.getenv("DBPASSWORD"))
DATABASE_NAME = str(os.getenv("DBNAME"))
DATABASE_PORT = str(os.getenv("DBPORT"))
DATABASE_HOST = str(os.getenv("DBHOST"))

conn_string = f'postgresql://'
conn_string += f'{DATABASE_USER}:{DATABASE_PASS}'
conn_string += f'@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'