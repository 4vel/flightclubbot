from aiogram import types
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import ReplyKeyboardRemove
from keyboards.default import menu

from loader import dp


@dp.message_handler(Command("menu"))
async def show_menu(message: types.Message):
    await message.answer("Выберите товар из меню ниже", reply_markup = menu)


@dp.message_handler(Text("Эспрессо"))
async def get_cotletki(message: types.Message):
    msg = """
    <b>Рецепт эспрессо.</b>
    18 грамм молотого кофе
    40 грамм воды
    """
    await message.answer(msg)


@dp.message_handler(Text(["Капучино"]))
async def show_menu(message: types.Message):
    msg = """
    <b>Рецепт капучино.</b>
    18 грамм молотого кофе
    40 мл воды
    120 мл молока
    """
    await message.answer(msg, reply_markup = ReplyKeyboardRemove())

@dp.message_handler(Text(["Латте"]))
async def show_menu(message: types.Message):
    msg = """
    <b>Рецепт Латте.</b>
    18 грамм молотого кофе
    40 мл воды
    200 мл молока
    """
    await message.answer(msg, reply_markup = ReplyKeyboardRemove())

@dp.message_handler(Text(["Ристретто"]))
async def show_menu(message: types.Message):
    msg = """
    <b>Рецепт Ристретто.</b>
    18 грамм молотого кофе
    20 мл воды
    """
    await message.answer(msg, reply_markup = ReplyKeyboardRemove())

@dp.message_handler(Text(["Кофе Раф"]))
async def show_menu(message: types.Message):
    msg = """
    <b>Рецепт Кофе Раф.</b>
    18 грамм молотого кофе
    20 мл воды
    """
    await message.answer(msg, reply_markup = ReplyKeyboardRemove())

@dp.message_handler(Text(["Лавандовый Раф"]))
async def show_menu(message: types.Message):
    msg = """
    <b>Рецепт Кофе Раф.</b>
    18 грамм молотого кофе
    20 мл воды
    """
    await message.answer(msg, reply_markup = ReplyKeyboardRemove())


@dp.message_handler(Text(["Эйр Латте"]))
async def show_menu(message: types.Message):
    msg = """
    <b>Рецепт Эйр Латте</b>
    18 грамм молотого кофе
    20 мл воды
    """
    await message.answer(msg, reply_markup = ReplyKeyboardRemove())

@dp.message_handler(Text(["Нитро Кофе"]))
async def show_menu(message: types.Message):
    msg = """
    <b>Рецепт Нитро Кофе</b>
    18 грамм молотого кофе
    20 мл воды
    """
    await message.answer(msg, reply_markup = ReplyKeyboardRemove())