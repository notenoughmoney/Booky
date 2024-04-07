import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from buttons import *

API_TOKEN = '7166275907:AAEu2PswJCooE_e2esz-mV9N7wEVBu3VvuI'
dp = Dispatcher()

# Настройка логгирования
logging.basicConfig(level=logging.INFO)

# Обработчик команды /start
@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Добро пожаловать! Выберите опцию из меню:", reply_markup=get_main_menu_buttons())

# Обработчик нажатий на кнопки
@dp.message(lambda message: message.text == "Моя библиотека")
async def process_button_click(message: types.Message):
    button_text = message.text
    await message.answer(f"Вы выбрали: {button_text}")
@dp.message(lambda message: message.text == "Рекомендации")
async def process_button_click(message: types.Message):
    button_text = message.text
    await message.answer(f"Вы выбрали: {button_text}")
@dp.message(lambda message: message.text == "Новинки")
async def process_button_click(message: types.Message):
    button_text = message.text
    await message.answer(f"Вы выбрали: {button_text}")
@dp.message(lambda message: message.text == "О нас")
async def process_button_click(message: types.Message):
    button_text = message.text
    await message.answer(f"Вы выбрали: {button_text}")

async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(API_TOKEN)
    # And the run events dispatching
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())