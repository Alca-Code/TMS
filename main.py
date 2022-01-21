# -*- coding: utf8 -*-
################################################################################################################################
import aiogram
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import BotBlocked
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
import making_json        ## ИМПОРТИРУЕМ ДАННЫЕ ИЗ ФАЙЛОВ making_json.py
import states           ##  ИМПОРТИРУЕМ ДАННЫЕ ИЗ ФАЙЛОВ states.py
######################

import logging # ПРОСТО ВЫВОДИТ В КОНСОЛЬ ИНФОРМАЦИЮ, КОГДА БОТ ЗАПУСТИТСЯ


storage = MemoryStorage() # FOR FSM
bot = Bot(token=config.botkey, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    )


# Открытие бота
@dp.message_handler(commands=['start'], state='*')
async def start_message(message: types.Message, state: FSMContext):
    joinedFile = open("user.txt","r")
    joinedUsers = set ()
    for line in joinedFile:
        joinedUsers.add(line.strip())

    if not str(message.chat.id) in joinedUsers:
        joinedFile = open("user.txt","a")
        joinedFile.write(str(message.chat.id)+ "\n")
        joinedUsers.add(message.chat.id)
        # await bot.send_message(message.from_user.id, text.adding_massage)
    # await bot.send_message(message.from_user.id, text.enter_link_message)
    await bot.send_message(message.chat.id, text = text.hello_messages)
    await bot.send_message(message.chat.id, text = text.privacy, reply_markup=keyboard.privacy_buttons, parse_mode='Markdown')
    privacy_doc = open('./docs/User_Agreement.docx', 'rb')
    await bot.send_document(chat_id=message.chat.id, document=privacy_doc)
    await states.User.Privacy.set()


@dp.message_handler(text = 'Да', state = states.User.Privacy) # МЫ ПРОПИСЫВАЛИ В КНОПКАХ КАЛЛБЭК "JOIN" ЗНАЧИТ И ТУТ МЫ ЛОВИМ "JOIN"
async def join(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, text = text.menu_text, reply_markup=keyboard.keyboard, parse_mode='Markdown')
    await states.User.Started_chat.set()

@dp.message_handler(text = 'Нет', state = states.User.Privacy)# МЫ ПРОПИСЫВАЛИ В КНОПКАХ КАЛЛБЭК "cancle" ЗНАЧИТ И ТУТ МЫ ЛОВИМ "cancle"
async def cancel(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, text= text.privacy_disagree, reply_markup=keyboard.privacy_buttons, parse_mode='Markdown')
    meme = open('./images/bye-im-out.gif', 'rb')
    await bot.send_animation(chat_id=message.chat.id,animation=meme)
    

# Ввод слова для поиска
@dp.message_handler(text=text.search_button, state=states.User.Started_chat)
async def search_button(message: types.Message, state: FSMContext):
        await bot.send_message(message.chat.id, text = text.about_search__button, reply_markup=keyboard.cancel_buttons, parse_mode='Markdown')
        await states.User.Search.set()


# Отмена ввода слова для поиска
@dp.message_handler(state=states.User.Search, text=text.cancel_button_text)
async def entering_link_cancel(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text.cancel_massage, reply_markup=keyboard.keyboard,
                           parse_mode="Markdown")
    await states.User.Started_chat.set()


# Информация о боте.
@dp.message_handler(state=states.User.Started_chat, text=text.about_bot_button_text)
async def about_bot_massage(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text.bot_info, reply_markup=keyboard.keyboard,
                           parse_mode="Markdown")
    await states.User.Started_chat.set()


#Запуск алгоритма поиска
@dp.message_handler(state=states.User.Search)
async def checking_site(message: types.Message, state: FSMContext):
   
        await bot.send_message(message.from_user.id, text.start_search, reply_markup=keyboard.cancel_buttons,
                               parse_mode="Markdown")

        ans = making_json.search_engine(making_json.a ,message.text)
        await bot.send_message(message.from_user.id, text.search_issue,
                                reply_markup=keyboard.cancel_buttons, parse_mode="Markdown")
        await bot.send_message(message.from_user.id, ans, reply_markup=keyboard.keyboard, parse_mode="Markdown")
        await states.User.Started_chat.set()
# Бот ошибся
@dp.message_handler(state=states.User.Started_chat, text=text.mistake_button)
async def bot_mistake(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text.about_mistake, reply_markup=keyboard.cancel_buttons,
                           parse_mode="Markdown")
    await states.User.Entering_bot_mistake.set()

# Отправка ошибки бота
@dp.message_handler(state=states.User.Entering_bot_mistake)
async def bot_mistake_entered(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text = text.sending_mistake, reply_markup=keyboard.cancel_buttons,
                           parse_mode="Markdown")
    await bot.send_message(246880643, "Сообщение модератору: " + message.text, reply_markup=keyboard.cancel_buttons,
                           parse_mode="Markdown")
    await states.User.Before_back.set()

 #Ввод не существующей команды
@dp.message_handler(state="*")
async def wrong_command(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text.wrong_command_text, reply_markup=keyboard.keyboard,
                           parse_mode="Markdown")
    await states.User.Started_chat.set()

#Кнопка Назад
@dp.message_handler(state="*", text=text.cancel_button_text)
async def bot_mistake_cancel(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Назад", reply_markup=keyboard.keyboard,
                           parse_mode="Markdown")
    await states.User.Started_chat.set()
    





##############################################################
if __name__ == '__main__':
    print('Бот в сети!')                                    # ЧТОБЫ БОТ РАБОТАЛ ВСЕГДА с выводом в начале вашего любого текста
executor.start_polling(dp, skip_updates=True)
##############################################################


