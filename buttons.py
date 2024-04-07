from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# Определение кнопок для главного меню
def get_main_menu_buttons():
    buttons = [
        [KeyboardButton(text="Моя библиотека"), KeyboardButton(text="Рекомендации")],
        [KeyboardButton(text="Новинки"), KeyboardButton(text="О нас")],
    ]
    reply_markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)
    return reply_markup


# Определение кнопок для ветки Моя библиотека
def get_library_menu_buttons():
    buttons = [
        [KeyboardButton(text="Добавить книгу")],
        [KeyboardButton(text="Назад")],
    ]
    reply_markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)
    return reply_markup
