import os
from aiogram import Dispatcher, executor, Bot
from aiogram.types import Message
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
import sqlite3
from keyboards import *

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = Bot(TOKEN, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Answer(StatesGroup):
    firstans = State()
    secans = State()
    thirdans = State()


@dp.message_handler(commands=['start'])
async def command_start(message: Message):
    await message.answer('Здравствуй, я бот который помогает тебе с покупками <b>техномарт</b>')
    await send_category_to_user(message)


async def send_category_to_user(message: Message):
    db = sqlite3.connect('texnomart.db')
    cursor = db.cursor()
    chat_id = message.chat.id
    cursor.execute('''
        SELECT category_name FROM categories
    ''')
    categories = cursor.fetchall()
    await Answer.firstans.set()
    await bot.send_message(chat_id, 'Выберите категорию: 👇', reply_markup=generate_categories(categories))


@dp.message_handler(state=Answer.firstans)
async def send_under_catalog_to_user(message: Message, state=FSMContext):
    chat_id = message.chat.id
    user_search = message.text
    db = sqlite3.connect('texnomart.db')
    cursor = db.cursor()
    cursor.execute('''
        SELECT under_catalog_name FROM under_catalogs WHERE category_name = ?
    ''', (user_search,))
    catalog_name = cursor.fetchall()
    await Answer.next()
    await bot.send_message(chat_id, 'Выберите подкатегорию: 👇', reply_markup=generate_categories(catalog_name))


@dp.message_handler(state=Answer.secans)
async def send_under_category_to_user(message: Message, state=FSMContext):
    chat_id = message.chat.id
    user_select = message.text
    db = sqlite3.connect('texnomart.db')
    cursor = db.cursor()
    cursor.execute('''
        SELECT under_category_name FROM under_categories WHERE under_catalog_name = ?
    ''', (user_select,))
    category_name = cursor.fetchall()
    await Answer.next()
    await bot.send_message(chat_id, 'Выберите подкатегорию: 👇', reply_markup=generate_categories(category_name))


@dp.message_handler(state=Answer.thirdans)
async def send_link_to_user(message: Message, state=FSMContext):
    chat_id = message.chat.id
    user_select2 = message.text
    db = sqlite3.connect('texnomart.db')
    cursor = db.cursor()
    cursor.execute('''
        SELECT under_category_link FROM under_categories WHERE under_category_name = ?
    ''', (user_select2,))
    try:
        user_link = cursor.fetchall()[0][0]
        await bot.send_message(chat_id, f'''✔ Ваш выбор:
    {user_link}
    ''', reply_markup=generate_inline_link(user_link, user_select2))
        print(f'''
Имя: {message.from_user.first_name} {message.from_user.last_name}
Username: {message.from_user.username}
Выбор: {user_link}
''')
        await send_category_to_user(message)
    except IndexError as e:
        await bot.send_message(chat_id, '''
    Причина появления данного сообщения:
1) Ты нажал на кнопку два раза
2) Ты решил написать что-то в чат
3) Товара в базе-данных нету
<i>Я перекину тебя на выбор категории, больше так не делай!</i>
''')
        await send_category_to_user(message)


executor.start_polling(dp, skip_updates=True)
