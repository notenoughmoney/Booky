import asyncio
import logging
import sys

from api import search_books_by_title
from db import *
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import CommandStart
from buttons import *

API_TOKEN = '7166275907:AAEu2PswJCooE_e2esz-mV9N7wEVBu3VvuI'
dp = Dispatcher()
router = Router()
dp.include_router(router)
db = SQLiteBooks()

# Настройка логгирования
logging.basicConfig(level=logging.INFO)


# States
class States(StatesGroup):
    MAIN_MENU = State()
    LIBRARY_MENU = State()
    RECS_MENU = State()
    NEW_BOOKS_MENU = State()
    ABOUT_MENU = State()
    ADD_BOOK = State()

# Обработчик команды /start
@router.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await message.answer("Добро пожаловать! Выберите опцию из меню:", reply_markup=get_main_menu_buttons())
    await state.set_state(States.MAIN_MENU)


@router.message(States.MAIN_MENU, F.text == "Моя библиотека")
async def process_button_click(message: types.Message, state: FSMContext):
    user = message.from_user.id
    read_books = db.get_read_books(user)
    await message.answer(text=f'{read_books}', reply_markup=get_library_menu_buttons())
    await state.set_state(States.LIBRARY_MENU)


@router.message(States.LIBRARY_MENU, F.text == "Добавить книгу")
async def process_button_click(message: types.Message, state: FSMContext):
    await message.answer(text='Чтобы добавить книгу в библиотеку, введите её название')
    await state.set_state(States.ADD_BOOK)


@router.message(States.ADD_BOOK, F.text != "")
async def process_button_click(message: types.Message, state: FSMContext):
    books = search_books_by_title(message.text)
    text = f"Книги найденные по запросу:"
    for book in books:
        text += "\n"
        text += f"\n№ {book["id_message"]}"
        text += f"\n{book["title"]}"
        text += f"\n{book["author"]}"
        text += f"\n{book["year"]}"
    await message.answer(text=text)
    await state.set_state(States.ADD_BOOK)


@router.message(States.MAIN_MENU, F.text == "Рекомендации")
async def process_button_click(message: types.Message, state: FSMContext):
    await message.answer(f"Этот раздел ещё недоступен")
    await state.set_state(States.RECS_MENU)


@router.message(States.MAIN_MENU, F.text == "Новинки")
async def process_button_click(message: types.Message, state: FSMContext):
    await message.answer(f"Этот раздел ещё недоступен")
    await state.set_state(States.NEW_BOOKS_MENU)


@router.message(States.MAIN_MENU, F.text == "О нас")
async def process_button_click(message: types.Message, state: FSMContext):
    await message.answer(f"Этот раздел ещё недоступен")
    await state.set_state(States.ABOUT_MENU)


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(API_TOKEN)
    # And the run events dispatching
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())