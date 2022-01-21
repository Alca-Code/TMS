# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


# keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
# link_enter_button = KeyboardButton(text.next_site_button_text)
# incorrect_bot_behavior = KeyboardButton(text.incorrect_bot_behavior_button_text)
# about_bot_button = KeyboardButton(text.about_bot_button_text)
# about_confidence_policy_button = KeyboardButton(text.about_policy_confidence_button_text)
# keyboard.add(link_enter_button).add(text.information_button_text).add(about_bot_button).add(
#     text.incorrect_bot_behavior_button_text)

# cancel_buttons = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
# cancel_buttons.add(KeyboardButton(text.cancel_button_text))

# information_buttons = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
# information_buttons.add(text.about_policy_confidence_button_text).add(text.about_frequent_violations_button_text) \
#     .add(KeyboardButton(text.cancel_button_text))

from re import search
from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import text
######################################################
# start = types.ReplyKeyboardMarkup(resize_keyboard=True) # СОЗДАЕМ ВООБЩЕ ОСНОВУ ДЛЯ КНОПОК
keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
info = types.KeyboardButton("Информация")            # ДОБАВЛЯЕМ КНОПКУ ИНФОРМАЦИИ
search_item = types.KeyboardButton(text.search_button)
about_bot_button = KeyboardButton(text.about_bot_button_text)

keyboard.add(text.search_button).add(about_bot_button).add(text.mistake_button)

privacy_buttons = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
privacy_agree = types.KeyboardButton('Да')
privacy_disagree = types.KeyboardButton('Нет')
privacy_buttons.add('Да').add('Нет')

cancel_buttons = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
cancel_buttons.add(KeyboardButton(text.cancel_button_text))

