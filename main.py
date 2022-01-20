# # import asyncio
# import aiogram
# import link
# from aiogram import Bot, Dispatcher, executor, types
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.dispatcher import FSMContext
# import config
# import states
# import text
# import keyboards
# import making_json
# import parsingPage
# bot = Bot(config.Token)
# dp = Dispatcher(bot, storage=MemoryStorage())

# # Начало работы приветствие
# @dp.message_handler(commands=['start'], state='*')
# async def start_message(message: types.Message, state: FSMContext):
#     await bot.send_message(message.from_user.id, text.hello_message,
#                            reply_markup=keyboards.keyboard,
#                            parse_mode="Markdown")
#     # await bot.send_message(message.from_user.id, text.adding_massage)
#     # await bot.send_message(message.from_user.id, text.enter_link_message)
#     await states.User.Started_chat.set()

# -*- coding: utf8 -*-
################################################################################################################################
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
#################################################################################################################################

######################################################################
from aiogram.dispatcher import FSMContext                            ## ТО, ЧЕГО ВЫ ЖДАЛИ - FSM
from aiogram.dispatcher.filters import Command                        ## ТО, ЧЕГО ВЫ ЖДАЛИ - FSM
from aiogram.contrib.fsm_storage.memory import MemoryStorage        ## ТО, ЧЕГО ВЫ ЖДАЛИ - FSM
from aiogram.dispatcher.filters.state import StatesGroup, State        ## ТО, ЧЕГО ВЫ ЖДАЛИ - FSM
######################################################################

######################
import config        ## ИМПОРТИРУЕМ ДАННЫЕ ИЗ ФАЙЛОВ config.py
import keyboard        ## ИМПОРТИРУЕМ ДАННЫЕ ИЗ ФАЙЛОВ keyboard.py
import text          ## ИМПОРТИРУЕМ ДАННЫЕ ИЗ ФАЙЛОВ text.py
######################

import logging # ПРОСТО ВЫВОДИТ В КОНСОЛЬ ИНФОРМАЦИЮ, КОГДА БОТ ЗАПУСТИТСЯ

storage = MemoryStorage() # FOR FSM
bot = Bot(token=config.botkey, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    )


@dp.message_handler(Command("start"), state=None)

async def welcome(message):
    joinedFile = open("user.txt","r")
    joinedUsers = set ()
    for line in joinedFile:
        joinedUsers.add(line.strip())

    if not str(message.chat.id) in joinedUsers:
        joinedFile = open("user.txt","a")
        joinedFile.write(str(message.chat.id)+ "\n")
        joinedUsers.add(message.chat.id)

    await bot.send_message(message.chat.id, f"ПРИВЕТ, *{message.from_user.first_name},* БОТ РАБОТАЕТ {text.hello_message} ", reply_markup=keyboard.start, parse_mode='Markdown')

@dp.message_handler(content_types=['text'])
async def get_message(message):
    if message.text == "Информация":
        await bot.send_message(message.chat.id, text = "Информация\nБот создан специально для моих любимых девочек и мальчиков с lzt ", parse_mode='Markdown')


    if message.text == "Статистика":
        await bot.send_message(message.chat.id, text = "Хочешь просмотреть статистику бота?", reply_markup=keyboard.stats, parse_mode='Markdown')


    if message.text == text.search_button:
        await bot.send_message(message.chat.id, text = text.about_search__button, reply_markup=keyboard.search, parse_mode='Markdown')


@dp.callback_query_handler(text_contains='join') # МЫ ПРОПИСЫВАЛИ В КНОПКАХ КАЛЛБЭК "JOIN" ЗНАЧИТ И ТУТ МЫ ЛОВИМ "JOIN"
async def join(call: types.CallbackQuery):
    if call.message.chat.id == config.admin:
        d = sum(1 for line in open('user.txt'))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Вот статистика бота: *{d}* человек', parse_mode='Markdown')
    else:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = "У тебя нет админки\n Куда ты полез", parse_mode='Markdown')



@dp.callback_query_handler(text_contains='cancle') # МЫ ПРОПИСЫВАЛИ В КНОПКАХ КАЛЛБЭК "cancle" ЗНАЧИТ И ТУТ МЫ ЛОВИМ "cancle"
async def cancle(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= "Ты вернулся В главное меню. Жми опять кнопки", parse_mode='Markdown')

##############################################################
if __name__ == '__main__':
    print('Бот в сети!')                                    # ЧТОБЫ БОТ РАБОТАЛ ВСЕГДА с выводом в начале вашего любого текста
executor.start_polling(dp)
##############################################################



































# storage = MemoryStorage() # FOR FSM
# bot = Bot(token=config.botkey, parse_mode=types.ParseMode.HTML)
# dp = Dispatcher(bot, storage=storage)

# logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
#                     level=logging.INFO,
#                     )

# @dp.message_handler(Command("start"), state=None)

# async def welcome(message):
#     joinedFile = open("user.txt","r")
#     joinedUsers = set ()
#     for line in joinedFile:
#         joinedUsers.add(line.strip())

#     if not str(message.chat.id) in joinedUsers:
#         joinedFile = open("user.txt","a")
#         joinedFile.write(str(message.chat.id)+ "\n")
#         joinedUsers.add(message.chat.id)

#     await bot.send_message(message.chat.id, f"ПРИВЕТ, *{message.from_user.first_name},* БОТ РАБОТАЕТ.{text.hello_message} ", reply_markup=keyboards.start, parse_mode='Markdown')


# @dp.message_handler(content_types=['text'])
# async def get_message(message):
#     if message.text == "Информация":
#         await bot.send_message(message.chat.id, text = "Информация\n Я студентческий бот проекта Trade Mark Security. Меня только создали, но я уже немного умею ", parse_mode='Markdown')
#     if message.text == "Статистика":
#         await bot.send_message(message.chat.id, text = "Хочешь просмотреть статистику бота?", reply_markup=keyboards.stats, parse_mode='Markdown')
#     # if message.text == text.search_button:
#     #     await bot.send_message(message.chat.id, text = text.about_search__button, reply_markup=keyboards.stats, parse_mode = "Markdown" )

# @dp.callback_query_handler(text_contains='join') # МЫ ПРОПИСЫВАЛИ В КНОПКАХ КАЛЛБЭК "JOIN" ЗНАЧИТ И ТУТ МЫ ЛОВИМ "JOIN"
# async def join(call: types.CallbackQuery):
#     if call.message.chat.id == config.admin:
#         d = sum(1 for line in open('user.txt'))
#         await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Вот статистика бота: *{d}* человек', parse_mode='Markdown')
#     else:
#         await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = "У тебя нет админки\n Куда ты полез", parse_mode='Markdown')



# @dp.callback_query_handler(text_contains='cancle') # МЫ ПРОПИСЫВАЛИ В КНОПКАХ КАЛЛБЭК "cancle" ЗНАЧИТ И ТУТ МЫ ЛОВИМ "cancle"
# async def cancle(call: types.CallbackQuery):
#     await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= "Ты вернулся В главное меню. Жми опять кнопки", parse_mode='Markdown')

# @dp.message_handler(state="*")
# async def wrong_command(message: types.Message, state: FSMContext):
#     await bot.send_message(message.from_user.id, text.wrong_command_text,
#                            parse_mode="Markdown")



# ##############################################################
# if __name__ == '__main__':
#     print('Бот в сети!')                                    # ЧТОБЫ БОТ РАБОТАЛ ВСЕГДА с выводом в начале вашего любого текста
# executor.start_polling(dp)
# ##############################################################

