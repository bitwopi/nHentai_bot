from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_home_reply_keyboard():
    home_reply_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    items = [KeyboardButton("Search🔎")]
    for item in items:
        home_reply_markup.insert(item)
    return home_reply_markup


def get_search_keyboard():
    search_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    items = [KeyboardButton("Cancel")]
    for item in items:
        search_keyboard.insert(item)
    return search_keyboard
