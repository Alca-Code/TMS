from aiogram.dispatcher.filters.state import State, StatesGroup


class User(StatesGroup):
    Started_chat = State()
    Privacy = State()
    Search = State()
    Entered_ref = State()
    Entering_bot_mistake = State()
    Before_back = State()
    Information = State()