from os import getenv
import redis

from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton)
from aiogram.utils.callback_data import CallbackData

from ..services import get_quiz

menu_cd = CallbackData("show_menu", "level", 'text', 'text2', 'text3')
bus_callback = CallbackData('schedule', 'level', 'd')

r = redis.Redis()

def make_callback_data_bus(level, d="0"):
    return bus_callback.new(level=level, d=d)


def make_callback_data(level, text='0', text2='0', text3='0'):
    return menu_cd.new(level=level, text=text, text2=text2, text3=text3)


async def main_keyboard(num):
    CURRENT_LEVEL = num
    items = await get_quiz()
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f"{await items[num].answer_1}",

                callback_data=make_callback_data(level=CURRENT_LEVEL + 1,
                                                 text=f"{await items[num].answer_1}")
            )]])
    markup.row(
        InlineKeyboardButton(
            text=f"{await items[num].answer_2}",
            callback_data=make_callback_data(level=CURRENT_LEVEL + 1,
                                             text=f"{await items[num].answer_2}")
        ))
    markup.row(
        InlineKeyboardButton(
            text=f"{await items[num].answer_3}",
            callback_data=make_callback_data(level=CURRENT_LEVEL + 1,
                                             text=f"{await items[num].answer_3}")
        ))
    markup.row(
        InlineKeyboardButton(
            text=f"{await items[num].answer_4}",
            callback_data=make_callback_data(level=CURRENT_LEVEL + 1,
                                             text=f"{await items[num].answer_4}")
        ))
    return markup


async def menu_markup():
    markup = await main_keyboard(0)
    return markup


async def markup_question_2():
    markup = await main_keyboard(1)
    return markup


async def markup_question_3():
    markup = await main_keyboard(2)
    return markup


async def solo_question_1():
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f'{r.get("answer1").decode("utf-8")}',

                callback_data=make_callback_data(level=CURRENT_LEVEL + 1,
                                                 text=f"{r.get('answer1').decode('utf-8')}")
            )]])
    markup.row(
        InlineKeyboardButton(
            text=f'{r.get("answer2").decode("utf-8")}',
            callback_data=make_callback_data(level=CURRENT_LEVEL + 1,
                                             text=f"{r.get('answer2').decode('utf-8')}")
        ))
    markup.row(
        InlineKeyboardButton(
            text=f'{r.get("answer3").decode("utf-8")}',
            callback_data=make_callback_data(level=CURRENT_LEVEL + 1,
                                             text=f"{r.get('answer3').decode('utf-8')}")
        ))
    markup.row(
        InlineKeyboardButton(
            text=f'{r.get("answer4").decode("utf-8")}',
            callback_data=make_callback_data(level=CURRENT_LEVEL + 1,
                                             text=f"{r.get('answer4').decode('utf-8')}")
        ))
    return markup


async def solo_question_2():
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f'{r.get("answer1").decode("utf-8")}',

                callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                                 text=f"{r.get('answer1').decode('utf-8')}")
            )]])
    markup.row(
        InlineKeyboardButton(
            text=f'{r.get("answer2").decode("utf-8")}',
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                             text=f"{r.get('answer2').decode('utf-8')}")
        ))
    markup.row(
        InlineKeyboardButton(
            text=f'{r.get("answer3").decode("utf-8")}',
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                             text=f"{r.get('answer3').decode('utf-8')}")
        ))
    markup.row(
        InlineKeyboardButton(
            text=f'{r.get("answer4").decode("utf-8")}',
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                             text=f"{r.get('answer4').decode('utf-8')}")
        ))
    return markup


menu_quiz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Викторина'),
            KeyboardButton(text='Розыгрыш')
        ],
[
            KeyboardButton(text='Результаты викторины'),
            KeyboardButton(text='Результаты розыгрыша'),
        ],
[
            KeyboardButton(text='Очистить списки'),
            KeyboardButton(text='Создать розыгрыш')
        ],
    ],
    resize_keyboard=True
)

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Расписане транспорта'),
            KeyboardButton(text='Коды расчетных'),
            KeyboardButton(text='Наборы в дк БЕЛАЗ')
        ],
[
            KeyboardButton(text='Услуги дк БЕЛАЗ'),
            KeyboardButton(text='График работы проходных'),

        ],
    ],
    resize_keyboard=True
)


async def schedule_bus():
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup(row_width=2)

    markup.insert(
        InlineKeyboardButton(text='От УГК НТЦ',
                             callback_data=make_callback_data_bus(level=CURRENT_LEVEL + 1, d='1'))
    )
    markup.insert(
        InlineKeyboardButton(text='От термогальванического цеха',
                             callback_data=make_callback_data_bus(level=CURRENT_LEVEL + 1, d='2'))
    )
    return markup


async def final_schedule(d):
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data_bus(level=CURRENT_LEVEL - 1, d=d))
    )
    return markup