from aiogram.dispatcher.filters.state import State, StatesGroup


class Question(StatesGroup):
    Q1 = State()
    a1 = State()
    a2 = State()
    a3 = State()
    a4 = State()
    ar = State()
