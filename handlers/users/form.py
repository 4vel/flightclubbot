from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp
from states.form import Form


@dp.message_handler(Command("form"))
async def enter_form(message: types.Message):
    msg = """
    Укажите направление для отслеживания цен на авиабилеты
    """
    await message.answer(msg)
    await message.answer("Укажите IATA код аэропорта \n")
    await Form.Q1.set()



@dp.message_handler(state=Form.Q1)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text

    await state.update_data(answer1=answer)
    await message.answer("Укажите максимальный порог цены в рублях \n")
    await Form.next()

@dp.message_handler(state=Form.Q3)
async def answer_q3(message: types.Message, state: FSMContext):
    data = await state.get_data()
    answer1 = data.get("answer1")
    answer2 = data.get("answer2")

    await message.answer("Добавили в список !")
    await message.answer(f"Аэропорт - {answer1}")
    await message.answer(f"Цена - {answer2}")
    await state.reset_state()
