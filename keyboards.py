from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

def generate_categories(categories):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = []
    for category in categories:
        btn = KeyboardButton(text=category[0])
        buttons.append(btn)

    markup.add(*buttons)
    return markup

def generate_inline_link(link, word):
    markup = InlineKeyboardMarkup() # callback_data - максимум 64 бит - 64 символа
    link = InlineKeyboardButton(text=f'Техномарт: {word}', url=link)
    markup.add(link)
    return markup

