# import asyncio
import aiogram
import link
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import config
import states
import text
import keyboards
import FindingPrivacypolicy
import PolicyChecking

bot = Bot(config.Token)
dp = Dispatcher(bot, storage=MemoryStorage())


# Начало работы приветствие
@dp.message_handler(commands=['start'], state='*')
async def start_message(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text.hello_message,
                           reply_markup=keyboards.keyboard,
                           parse_mode="Markdown")
    # await bot.send_message(message.from_user.id, text.adding_massage)
    # await bot.send_message(message.from_user.id, text.enter_link_message)
    await states.User.Started_chat.set()


# Ввод ссылки на сайт
@dp.message_handler(text=text.next_site_button_text, state=states.User.Started_chat)
async def enter_link_message(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text.enter_link_message, reply_markup=keyboards.cancel_buttons,
                           parse_mode="Markdown")
    await states.User.Entering_link.set()


# Отмена ввода ссылки
@dp.message_handler(state=states.User.Entering_link, text=text.cancel_button_text)
async def entering_link_cancel(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text.entering_link_cancel_massage, reply_markup=keyboards.keyboard,
                           parse_mode="Markdown")
    await states.User.Started_chat.set()


# Проверка ссылки и вывод информации о политики конфеденциальности
@dp.message_handler(state=states.User.Entering_link)
async def checking_site(message: types.Message, state: FSMContext):
    if link.validate_link(message.text):
        await bot.send_message(message.from_user.id, text.link_is_correct, reply_markup=keyboards.cancel_buttons,
                               parse_mode="Markdown")
        # await states.User.Entered_ref.set()
        # Проверка политики конфеденциальности.
        ans = FindingPrivacypolicy.have_confidence_police(message.text)
        if ans[0]:
            await bot.send_message(message.from_user.id, text.has_confidence_politic,
                                   reply_markup=keyboards.cancel_buttons, parse_mode="Markdown")
            await bot.send_message(message.from_user.id, ans[1][-1], reply_markup=keyboards.cancel_buttons)
            await bot.send_message(message.from_user.id, text.about_criteria)
            await bot.send_message(message.from_user.id, PolicyChecking.check_criteria(ans[1][-1]),
                                   reply_markup=keyboards.cancel_buttons, parse_mode="Markdown")
        else:
            root = link.get_root_link(message.text)
            if root[0]:
                ans = FindingPrivacypolicy.have_confidence_police(root[1])
                if ans[0]:
                    await bot.send_message(message.from_user.id, text.has_confidence_politic,
                                           reply_markup=keyboards.cancel_buttons, parse_mode="Markdown")
                    await bot.send_message(message.from_user.id, ans[1][-1], reply_markup=keyboards.cancel_buttons)
                    await bot.send_message(message.from_user.id, text.about_criteria)
                    await bot.send_message(message.from_user.id, PolicyChecking.check_criteria(ans[1][-1]),
                                           reply_markup=keyboards.cancel_buttons, parse_mode="Markdown")

                else:
                    await bot.send_message(message.from_user.id, text.has_no_confidence_politic,
                                           reply_markup=keyboards.cancel_buttons, parse_mode="Markdown")
            else:
                await bot.send_message(message.from_user.id, text.has_no_confidence_politic,
                                       reply_markup=keyboards.cancel_buttons, parse_mode="Markdown")

        await states.User.Before_back.set()
    else:
        await bot.send_message(message.from_user.id, text.link_is_incorrect,
                               reply_markup=keyboards.cancel_buttons, parse_mode="Markdown")
        await states.User.Entering_link.set()


# Информация о политике конфиденсальности.
@dp.message_handler(state=states.User.Information, text=text.about_policy_confidence_button_text)
async def about_confidence_policy_massage(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text.about_policy_confidence_massage,
                           reply_markup=keyboards.information_buttons,
                           parse_mode="Markdown")
    await states.User.Information.set()


# Информация о  наиболее частых нарушениях.
@dp.message_handler(state=states.User.Information, text=text.about_frequent_violations_button_text)
async def about_frequent_violations(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text.about_frequent_violations_message,
                           reply_markup=keyboards.information_buttons,
                           parse_mode="Markdown")
    await states.User.Information.set()


# Информация о боте.
@dp.message_handler(state=states.User.Started_chat, text=text.about_bot_button_text)
async def about_bot_massage(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text.adding_massage, reply_markup=keyboards.cancel_buttons,
                           parse_mode="Markdown")
    await states.User.Before_back.set()


# Бот ошибся
@dp.message_handler(state=states.User.Started_chat, text=text.incorrect_bot_behavior_button_text)
async def bot_mistake(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text.enter_bot_mistake_massage, reply_markup=keyboards.cancel_buttons,
                           parse_mode="Markdown")
    await states.User.Entering_bot_mistake.set()


# Переход в раздел информации
@dp.message_handler(state=states.User.Started_chat, text=text.information_button_text)
async def to_information(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text.information_button_text,
                           reply_markup=keyboards.information_buttons,
                           parse_mode="Markdown")
    await states.User.Information.set()


# Отмена (ввода ошибки) - любая
@dp.message_handler(state="*", text=text.cancel_button_text)
async def bot_mistake_cancel(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Назад", reply_markup=keyboards.keyboard,
                           parse_mode="Markdown")
    await states.User.Started_chat.set()


# Ошибка бота введена
@dp.message_handler(state=states.User.Entering_bot_mistake)
async def bot_mistake_entered(message: types.Message, state: FSMContext):
    await bot.send_message(407036466, "Сообщение модератору: " + message.text, reply_markup=keyboards.cancel_buttons,
                           parse_mode="Markdown")
    await bot.send_message(91813495, "Сообщение модератору: " + message.text, reply_markup=keyboards.cancel_buttons,
                           parse_mode="Markdown")
    await bot.send_message(message.from_user.id, text.entered_bot_mistake_massage, reply_markup=keyboards.cancel_buttons,
                           parse_mode="Markdown")
    # Здесь можно сделать отправку оператору
    await states.User.Before_back.set()


# Команда не существует
@dp.message_handler(state="*")
async def wrong_command(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text.wrong_command_text,
                           parse_mode="Markdown")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
