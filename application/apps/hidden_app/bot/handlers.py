
from collections import defaultdict
from datetime import datetime
from os import getenv
from typing import Union
import redis

from aiogram import Dispatcher, bot
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ParseMode, InputFile, ChatMember, ChatMemberMember

from .keyboards import menu_markup, markup_question_2, menu_cd, bus_callback, markup_question_3, solo_question_2, menu, \
    schedule_bus, final_schedule, menu_quiz, solo_question_1
from .states import Question
from ..services import get_quiz, ger_answer
from ...core.services import get_user


r = redis.Redis()


def register_handlers(dp: Dispatcher):
    # Register your handlers here
    dp.register_message_handler(simple_doc, text=["Коды расчетных"])
    dp.register_message_handler(dk, text=["Наборы в дк БЕЛАЗ"])
    dp.register_message_handler(clear_list, text=["Очистить списки"])
    dp.register_message_handler(schedule_kpp, text=["График работы проходных"])
    dp.register_message_handler(dk_info, text=["Услуги дк БЕЛАЗ"])
    #dp.register_message_handler(type_of_operation, text=["Типы операций"])
    #dp.register_message_handler(general_workshop, text=["Общецеховая информация"])
    dp.register_message_handler(show_menu, text=['Викторина'])
    dp.register_message_handler(show_schedule, text=['Расписане транспорта'])
    dp.register_message_handler(start_solo, text=['Розыгрыш'])
    dp.register_message_handler(result, text=['Результаты викторины'])
    dp.register_message_handler(result_single, text=['Результаты розыгрыша'])
    dp.register_message_handler(show_main_menu, commands=["menu"])
    dp.register_message_handler(show_quiz_menu, commands=["menu_quiz"])
    #dp.register_callback_query_handler(navigate, menu_cd.filter())
    dp.register_callback_query_handler(nav, menu_cd.filter())
    dp.register_callback_query_handler(nav_schedule, bus_callback.filter())
    dp.register_message_handler(create_quiz, text=['Создать розыгрыш'])
    dp.register_message_handler(create_first_answer, state=Question.Q1)
    dp.register_message_handler(create_2_answer, state=Question.a1)
    dp.register_message_handler(create_3_answer, state=Question.a2)
    dp.register_message_handler(create_4_answer, state=Question.a3)
    dp.register_message_handler(create_right_answer, state=Question.a4)
    dp.register_message_handler(end_create, state=Question.ar)


winners = defaultdict(list)
winners_solo = defaultdict(list)
losers_solo = defaultdict(list)
# Create your handlers here


async def create_quiz(message: Message):
    await message.answer('Напишите вопрос')
    await Question.Q1.set()


async def create_first_answer(message: Message, state: FSMContext):
    question = message.text
    r.set('question', question)
    await state.update_data(question = question)
    await message.answer('Напишите Первый вариант ответа')
    await Question.a1.set()


async def create_2_answer(message: Message, state: FSMContext):
    answer1 = message.text
    r.set('answer1', answer1)
    await state.update_data(answer1 = answer1)
    await message.answer('Напишите второй вариант ответа')
    await Question.a2.set()


async def create_3_answer(message: Message, state: FSMContext):
    answer2 = message.text
    r.set('answer2', answer2)
    await state.update_data(answer2 = answer2)
    await message.answer('Напишите третий вариант ответа')
    await Question.a3.set()

async def create_4_answer(message: Message, state: FSMContext):
    answer3 = message.text
    r.set('answer3', answer3)
    await state.update_data(answer3 = answer3)
    await message.answer('Напишите четвертый вариант ответа')
    await Question.a4.set()

async def create_right_answer(message: Message, state: FSMContext):
    answer4 = message.text
    r.set('answer4', answer4)
    await state.update_data(answer4 = answer4)
    await message.answer('Напишите правильный ответ')
    await Question.ar.set()

async def end_create(message: Message, state: FSMContext):
    right_answer = message.text
    r.set('right_answer', right_answer)
    await state.update_data(right_answer=right_answer)
    await message.answer('Готово!')
    await state.finish()


async def simple_doc(message: Message):
    await message.answer_document(InputFile('C:\\Users\\Astro\\PycharmProjects\\aiogram-django\\doc\\Коды.pdf'))


async def clear_list(message: Message):
    winners_solo.clear()
    losers_solo.clear()
    await message.answer('Списки пользователей очищены')


async def schedule_kpp(message: Message):
    await message.answer('КПП № 1 - КРУГЛОСУТОЧНО\nКПП № 3a - 6:00-01.20\nКПП № 5 - 5:00-01.20\nКПП № 11 - 5:00-01.20\nКПП № 17 - 6:00-17.30\nКПП № 18 - 6:00-16.30\nКПП № 20 - 6:00-01.00\n')


async def dk(message: Message):
    await message.answer_photo(InputFile('C:\\Users\\Astro\\PycharmProjects\\aiogram-django\\doc\\nabor.jpg'))


async def dk_info(message: Message):
    await message.answer('Торжественная церемония регистрации брака''\n'
'Юбилеи предприятий, профессиональные праздники''\n'
'Презентации''\n'
'Шоу-конкурсы, театрализованные шоу''\n'
'Детские Дни рождения''\n'
'Народные фольклорные праздники''\n'
'Вечера отдыха, танцевально-развлекательные программы''\n'
'Услуги бильярдного зала''\n'
'Концерты''\n'
'Выпускные вечера''\n'
'Услуги студии звукозаписи''\n'
'Услуги проката''\n'
'Услуги библиотеки''\n'
'Ксерокопия''\n'
'Постановка свадебного танца''\n'
'Новогоднее поздравление Деда Мороза и Снегурочки''\n'
'Детские праздники и многое другое''\n'
'Персона для контакта''\n'
'По организации культурно-массовых мероприятий -''\n'
'Директор Дворца культуры:''\n''\n'
'СМОЛЬСКИЙ Геннадий Анатольевич''\n''\n''\n'


'Контактные телефоны:''\n'
'8 01775-4-85-42''\n''\n'

'Факс:''\n'
'8 01775-4-93-96''\n''\n'

'Приглашаем вас к взаимовыгодному сотрудничеству.')


async def show_menu(message: Union[CallbackQuery, Message], **kwargs):
    markup = await menu_markup()
    items = await get_quiz()
    text = str(items[0])
    if isinstance(message, Message):
        await message.answer(text=text, reply_markup=markup, parse_mode=ParseMode.HTML)
    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.edit_reply_markup(markup)


async def show_question_2(callback: CallbackQuery, answer, **kwargs):
    if callback.from_user.first_name in winners.keys():
        if len(winners[callback.from_user.first_name]) >= 4:
            pass
    else:
        winners[callback.from_user.first_name].append(answer)
        print(winners)
    markup = await markup_question_2()
    items = await get_quiz()
    text = str(items[1])
    await callback.message.edit_text(text=text, reply_markup=markup, parse_mode=ParseMode.HTML)


async def show_question_3(callback: CallbackQuery, answer2 ,**kwargs):
    if callback.from_user.first_name in winners.keys():
        if len(winners[callback.from_user.first_name]) >= 4:
            pass
        else:
            winners[callback.from_user.first_name].append(answer2)
            print(winners)
    markup = await markup_question_3()
    items = await get_quiz()
    text = str(items[2])
    await callback.message.edit_text(text=text, reply_markup=markup, parse_mode=ParseMode.HTML)


async def finish1(callback: CallbackQuery, answer3, **kwargs):
    if callback.from_user.first_name in winners.keys():
        if len(winners[callback.from_user.first_name]) >= 4:
            pass
        else:
            winners[callback.from_user.first_name].append(answer3)
            time = str(datetime.now())
            winners[callback.from_user.first_name].append(str(time[11:-7]))
            print(winners)
    answers = await ger_answer()
    async def ffe():
        if 'True' in winners[callback.from_user.first_name]:
            pass
        else:
            for i in range(3):
                if str(answers[i]) in winners[callback.from_user.first_name]:
                    winners[callback.from_user.first_name][i]='True'
                else:
                    winners.pop(callback.from_user.first_name)
                    break
        print(winners)
    await ffe()
    await callback.message.edit_text(text= 'Спасибо за участие, скоро мы объявим результаты', parse_mode=ParseMode.HTML)


async def result(message: Message):
    sorted_winners = dict(sorted(winners.items(), key=lambda x: x[1]))
    print(sorted_winners)
    first = list(sorted_winners.keys())[0]
    #second = list(sorted_winners.keys())[1]
    #third = list(sorted_winners.keys())[2]
    for user in sorted_winners.keys():
        a =sorted_winners[user][3]
        await message.answer(f"{user} Время: {a}")


async def navigate(cal: CallbackQuery, callback_data : dict):
    current_level = callback_data.get("level")
    answer = callback_data.get("text")
    answer2 = callback_data.get('text')
    answer3 = callback_data.get('text')


    levels = {
        "0": show_menu,
        "1": show_question_2,
        "2": show_question_3,
        "3": finish1

    }
    current_level_function = levels[current_level]
    await current_level_function(cal, answer=answer, answer2=answer2, answer3=answer3)


async def start_solo(message: Union[CallbackQuery, Message], **kwargs):
    markup = await solo_question_1()
    text=f'{r.get("question").decode("utf-8")}'
    #await message.bot.send_message(chat_id='-1001608043243', text=text, reply_markup=markup)
    await message.answer(text=text, reply_markup=markup)


async def solo_question(message: Union[CallbackQuery, Message],answer, **kwargs):
    markup = await solo_question_1()
    if isinstance(message, Message):
        await message.answer(reply_markup=markup, parse_mode=ParseMode.HTML)
    elif isinstance(message, CallbackQuery):
        call = message
        if call.from_user.id in (winners_solo.keys() or losers_solo.keys()):
            await call.answer(f'Вы уже отвечали')
        else:
            if str(r.get("right_answer").decode("utf-8")) == answer:
                winners_solo[call.from_user.id].append(answer)
                time = str(datetime.now())
                winners_solo[call.from_user.id].append(str(time[11:-7]))
                winners_solo[call.from_user.id].append(call.from_user.first_name)
                await call.answer(f'Ваш ответ: {answer} принят')
            else:
                losers_solo[call.from_user.id].append(answer)
                await call.answer(f'Ваш ответ: {answer} принят')
        print(winners_solo, 'Winners')
        print(losers_solo, 'Losers')
        await call.message.edit_reply_markup(markup)


async def single_question(message: Union[CallbackQuery, Message], answer, **kwargs):
    markup = await solo_question_2()
    if isinstance(message, Message):
        await message.answer(reply_markup=markup, parse_mode=ParseMode.HTML)
    elif isinstance(message, CallbackQuery):
        call = message
        if call.from_user.id in (winners_solo.keys() or losers_solo.keys()):
            await call.answer(f'Вы уже отвечали')
        else:
            if str(r.get("right_answer").decode("utf-8")) == answer:
                winners_solo[call.from_user.id].append(answer)
                time = str(datetime.now())
                winners_solo[call.from_user.id].append(str(time[11:-7]))
                winners_solo[call.from_user.id].append(call.from_user.first_name)
                await call.answer(f'Ваш ответ: {answer} принят')
            else:
                losers_solo[call.from_user.id].append(answer)
                await call.answer(f'Ваш ответ: {answer} принят')
        print(winners_solo, 'Winners')
        print(losers_solo, 'Losers')
        await call.message.edit_reply_markup(markup)


async def result_single(message: Message):
    sorted_winners = dict(sorted(winners_solo.items(), key=lambda x: x[1]))
    print(sorted_winners)
    for i in range(5):
        text = list(sorted_winners.keys())[i]
        answer = sorted_winners[text][0]
        time = sorted_winners[text][1]
        username = sorted_winners[text][2]
        await message.answer(text=f"{username}, id:{text}, Ответ: {answer}, Время: {time}")


async def nav(cal: CallbackQuery, callback_data: dict):
    current_level = callback_data.get("level")
    answer = callback_data.get("text")
    levels = {
        "0": solo_question,
        "1": single_question,

    }
    current_level_function = levels[current_level]
    await current_level_function(cal, answer=answer)


async def show_main_menu(message: Message):
    a = await message.bot.get_chat_member(chat_id='-1001608043243', user_id=866100005)
    print(a['status'])
    await message.answer('Меню', reply_markup=menu)


async def show_quiz_menu(message: Message):
    await message.answer('Меню розыгрышей', reply_markup=menu_quiz)


async def show_schedule(message: Union[CallbackQuery, Message], **kwargs):
    markup = await schedule_bus()
    text = str('Расписание')
    if isinstance(message, Message):
        await message.answer(text=text, reply_markup=markup, parse_mode=ParseMode.HTML)
    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.edit_reply_markup(markup)


async def show_schedule_2(callback: CallbackQuery, d, **kwargs):
    markup = await final_schedule(d)
    if d == '2':
        text = str('От термогальванического цеха\n10:45\n13:45')
    else:
        text = str('От УГК НТЦ\n9:45\n12:45')
    await callback.message.edit_text(text=str(text), reply_markup=markup, parse_mode=ParseMode.HTML)


async def nav_schedule(cal: CallbackQuery, callback_data: dict):
    current_level = callback_data.get("level")
    d = callback_data.get("d")
    levels = {
        "0": show_schedule,
        "1": show_schedule_2,

    }
    current_level_function = levels[current_level]
    await current_level_function(cal, d=d)


async def type_of_operation(message: Message):
    await message.answer('01: Окраска\n02: ТВЧ\n03: Мех.Обработка\n04: МБ\n05: ОВК\n06: Заг-ный\n07: САПР\n08: Дробеструй\n09: Розница\n10: ПКП\n11: БТСТ\n12: УЗО\n13: МБТ\n14: ТНП\n15: СЗЦ\n16: ЗИП\n')


async def general_workshop(message: Message):
    user = await get_user()
    for id in user:
        print(id.tg_id)
        if message.from_user.id == id.tg_id:
            text = "/030 - Прессовый цех\n040 - Автоматный цех\n050 - Сварочный цех\n051 - Цех сварных конструкций (ЦСК)\n060 - Цех главного конвеера (ЦГК)\n070 - Термогальвонический цех\n080 - Цех механизации производства и станкостроения (ЦМПС)\n090 - Цех гидроагрегатов (ЦГА)\n100 - Механосборочный цех №1 (МСЦ-1)\n"
            break
        else:
            text='У вас нет доступа к этой информации'
    await message.answer(text=text)