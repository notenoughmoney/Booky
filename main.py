import asyncio
import logging
import sys

from api import search_books_by_title, get_newest_books
from db import *
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import CommandStart
from buttons import *

API_TOKEN = '7166275907:AAEu2PswJCooE_e2esz-mV9N7wEVBu3VvuI'
bot = Bot(API_TOKEN)
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
    GET_VIP_MENU = State()
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
    if len(read_books) < 1:
        text = "У вас ещё нет прочитанных книг"
    else:
        text = "Книги, которые вы прочитали:"
        for counter, book in enumerate(read_books):
            text += "\n\n№ " + str(counter)
            text += f'\n{book["title"]}'
            text += f'\n{book["author"]}'
    await message.answer(text=text, reply_markup=get_library_menu_buttons())
    await state.set_state(States.LIBRARY_MENU)


@router.message(States.LIBRARY_MENU, F.text == "Добавить книгу")
async def process_button_click(message: types.Message, state: FSMContext):
    # Сначала проверяем лимит доступных книг
    user = message.from_user.id
    user_status = db.get_user_status(user)
    read_books_count = db.get_read_books_count(user)
    if user_status != "VIP" and read_books_count >= 7:
        await message.answer(text='Для 111 получения дополнительных функций вам необходим VIP-статус')
        # ПРОДУБЛИРОВАТЬ
        await bot.send_invoice(
            message.chat.id,
            title="Стать VIP",
            description="С VIP можно сохранять больше книг",
            provider_token="1744374395:TEST:6b4eada6f5510967807d",
            currency="rub",
            photo_url="https://www.nme.com/wp-content/uploads/2016/11/RyanGoslingGettyImages-531518458.jpg",
            photo_width=315,
            photo_height=200,
            prices=[price],
            payload="test-invoice-payload"
        )
    else:
        await message.answer(text='Чтобы добавить книгу в библиотеку, введите её название')
        await state.set_state(States.ADD_BOOK)


@router.message(States.LIBRARY_MENU, F.text == "Назад")
async def process_button_click(message: types.Message, state: FSMContext):
    await message.answer(text='Главное меню.\nВыберите опцию из меню:', reply_markup=get_main_menu_buttons())
    await state.set_state(States.MAIN_MENU)


@router.message(States.ADD_BOOK, F.text != "")
async def process_button_click(message: types.Message, state: FSMContext):
    books = search_books_by_title(message.text)
    # TODO Проверку на уникальность книг
    db.add_book(
        user=message.from_user.id,
        title=books[0]["title"],
        author=books[0]["author"],
        year=books[0]["year"]
    )
    book = books[0]
    text = f"В вашу библиотеку была добавлена книга:"
    text += f'\n{book["title"]}'
    text += f'\n{book["author"]}'
    await message.answer(text=text)
    await state.set_state(States.LIBRARY_MENU)


@router.message(States.MAIN_MENU, F.text == "Рекомендации")
async def process_button_click(message: types.Message, state: FSMContext):
    user = message.from_user.id
    recs = db.get_recommendations(user=user)
    text = "Подборка на основе ваших предпочтений:"
    if len(recs) < 1:
        text = "К сожалению, мы не смогли подобрать для вас ничего подходящего..."
    else:
        for counter, book in enumerate(recs):
            counter += 1
            text += "\n\n№ " + str(counter)
            text += f'\n{book["title"]}'
            text += f'\n{book["author"]}'
    await message.answer(text=text)


@router.message(States.MAIN_MENU, F.text == "Новинки")
async def process_button_click(message: types.Message, state: FSMContext):
    user = message.from_user.id
    newest_books = get_newest_books(user)
    text = "Новинки книг, которые вы могли пропустить:"
    for counter, book in enumerate(newest_books):
        text += "\n\n№ " + str(counter)
        text += f'\n{book["title"]}'
        text += f'\n{book["author"]}'
    await message.answer(text=text)


@router.message(States.MAIN_MENU, F.text == "О нас")
async def process_button_click(message: types.Message, state: FSMContext):
    about_file = "about.txt"
    text = "Этот раздел временно недоступен"
    try:
        with open(about_file, 'r', encoding='utf-8') as file:
            text = file.read()
    except FileNotFoundError:
        pass
    except Exception as e:
        pass
    await message.answer(text=text)

price = types.LabeledPrice(label="Стать VIP", amount=10*100)
@router.message(States.MAIN_MENU, F.text == "Стать VIP")
async def send_invoice(message: types.Message, state: FSMContext):
    # ПРОДУБЛИРОВАТЬ
    await bot.send_invoice(
        message.chat.id,
        title="Стать VIP",
        description="С VIP можно сохранять больше книг",
        provider_token="1744374395:TEST:6b4eada6f5510967807d",
        currency="rub",
        photo_url="img.png",
        prices=[price],
        payload="test-invoice-payload"
    )


@router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@router.message(F.successful_payment)
async def successful_payment_handler(message: types.Message):
    user = message.from_user.id
    await message.answer(text="Оплата прошла успешо.\nВы получили статус VIP и можете сохранять больше книг!")
    db.make_vip(user=user)


async def main() -> None:
    # Run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
