from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup


def get_inline_search_keyboard():
    inline_markup = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton("Search by name🔎", switch_inline_query_current_chat=''),
        InlineKeyboardButton("Popular🔥", switch_inline_query_current_chat='🔥'),
        InlineKeyboardButton("Random🔀", callback_data="random")
    ]
    for button in buttons:
        inline_markup.insert(button)
    return inline_markup


def get_inline_card_keyboard(url: str, d_id: int):
    inline_markup = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton("Get images📸", callback_data="images"),
        InlineKeyboardButton("Download PDF", url="https://hiken.xyz/g/"+str(d_id)),
        InlineKeyboardButton("Read Online", url=url)
    ]
    for button in buttons:
        inline_markup.insert(button)
    return inline_markup
