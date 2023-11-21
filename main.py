from calendar import Calendar
import datetime

import sqlite3
from test import *
from calendar_func import *
from buttons_func import *

import telebot as tbt
from telebot import TeleBot



connect = sqlite3.connect('db_mvp.db')
cursor = connect.cursor()

cursor.execute('''
            CREATE TABLE IF NOT EXISTS INFO(
                date CHAR,
                info CHAR
            );
        ''')
connect.commit()

cursor.execute('''
            CREATE TABLE IF NOT EXISTS USERS(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tgtoken STR,
                isheadman INT
            );
        ''')
connect.commit()

def add_user_n(tgtoken):

    us_id = str(tgtoken)
    ishead = 0
    cur = cursor.connection("db_mvp.db")
    cur.execute(
        f'INSERT INTO USERS(tgtoken, isheadman) VALUES(?, ?)', (us_id, ishead)
    )
    connect.commit()


def get_calendar(MONTH, YEAR):
    return Calendar().itermonthdays(YEAR, MONTH)
API_TOKEN = ""

bot = TeleBot(API_TOKEN)

# Функция info
info_button = tbt.types.KeyboardButton(text="Календарь")
info_markup = tbt.types.ReplyKeyboardMarkup(resize_keyboard=True).add(info_button)
info_markup2 = tbt.types.ReplyKeyboardMarkup(resize_keyboard=True).add(info_button)

add_mode = 0 # Находится ли пользователь в состоянии добавления информации? 0 или 1

# Подтверждение
yes_button = tbt.types.KeyboardButton(text="Да")
no_button = tbt.types.KeyboardButton(text="Нет")
add_final_markup = tbt.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(yes_button, no_button)

# Информация + роль пользователя
date = str()
information = str()
role = str()

# Calendar
today = datetime.date.today().timetuple()
MONTH = today[1]
DAY = today[2]
YEAR = today[0]

month_names = {1:"Январь", 2:"Февраль", 3:"Март", 4:"Апрель",
               5:"Май", 6:"Июнь", 7:"Июль", 8:"Август",
               9:"Сентябрь", 10:"Октябрь", 11:"Ноябрь", 12:"Декабрь"}


@bot.message_handler(commands=["start"])
def start_message(message):
    tgtoken = message.from_user.id
    bot.reply_to(message, "Это OneSeven_Bot, бот для удобного поиска информации по классу в школе.\n"
                                "Для начала выберите свою роль", reply_markup=gen_startbuttons())

    ######################          РАБОТАЕТ+
    if check_user(message.from_user.id) == 1:
        add_user(str(message.from_user.id), 0)


@bot.callback_query_handler(lambda call: True)
def answer(call):
    global calendar_markup, DAY, MONTH, YEAR, date
    m = MONTH
    d = call.data
    print(call)
    if (len(call.data) == 1) and (call.data != "None"):
        d = int("0" + call.data)
    if len(str(MONTH)) == 1:
        m = int("0" + str(MONTH))
    date = f"{d}.{m}.{YEAR}"
    try:
        # role_dependence()
        if int(call.data) in range(32):
            bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                          message_id=call.message.id, reply_markup=None)
            if role == "user": # Отправляет информацию пользователю ~ adworm
                bot.send_message(call.message.chat.id,
                                 text=f"Выбрана дата {date}. Отправляем информацию:") # Все работает но может есть смысл сменить на date
                # all_info = get_info(date)
                text_for_write = ''''''

                for i in get_info(date):
                    text_for_write += f'\n{i}'

                bot.send_message(call.message.chat.id, f'{text_for_write}')

            elif role == "mod":
                #########################################   Тут был косяк     v   из-за чего неправильно выводилась дата (кажется сейчас все нормально)
                bot.send_message(call.message.chat.id, text=f"Выбрана дата {date}. Что делать с информацией?", reply_markup=gen_addread())
    except ValueError:
        print("Excepted ValueError")
    if call.data == ">>":
        if MONTH != 12:
            DAY = 1
            MONTH += 1
        else:
            DAY = 1
            MONTH = 1
            YEAR += 1
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id,
                                      reply_markup=inline_calendar(MONTH, YEAR,
                                                                   user_id=call.message.from_user.id))
    elif call.data == "<<":
        if MONTH != 1:
            DAY = 1
            MONTH -= 1
        else:
            DAY = 1
            MONTH = 12
            YEAR -= 1
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id,
                                      reply_markup=inline_calendar(MONTH, YEAR,
                                                                   user_id=call.message.from_user.id))


@bot.message_handler(content_types=['text'])
def user_text(message):
    global role, information, add_mode, date
    ######  Это надо (на будущее если я не ошибаюсь можно написать: global role, information, add_mode, date) выглядит лучше(наверное, а может и нет)
    if message.text == "Пользователь":
        role = "user"
        bot.send_message(message.chat.id, text="Теперь вы пользователь.\nНажмите на кнопку календарь, чтобы выбрать дату дня, информацию которого вы хотите получить", reply_markup=gen_info())
    if add_mode == 1: # Пропишите здесь проверку по бд на модератора ~ adworm
        # information = message.text     ВОТ ТАК БЫЛО

        ######################### А ЭТО Я СДЕЛАЛ
        if message.text != 'Да': information = message.text
        #########################

        bot.reply_to(message, text=f"Вы добавили информацию: " 
                                   f"{information}. \nВы уверены?", reply_markup=add_final_markup)
        print(information)


        ###############################  Вроде работает(бот дублирует сообщения о подтверждении, делает что-то непонятное, но бд исправно пополняется(но он иногда меняет инфу на ДА))
        ###############################  Думаю какой-то косяк с add_mode но я хз как он работает и где меняется а потому ничего не трогаю
        ###############################  РАБОТАЕТ (требуется доп. проверка)
        # add_info(message.chat.id, date, information)


        add_mode = 0
    elif message.text == "Дежурный": # Пропишите здесь проверку по бд на модератора ~ adworm
        role = "mod"
        bot.send_message(message.chat.id, text="Теперь вы дежурный.\nНажмите на кнопку календарь, чтобы выбрать дату дня, на который вы хотите добавить/изменить информацию", reply_markup=gen_info())
    elif message.text == "Календарь":
        bot.send_message(message.chat.id, text="Выберите день из календаря",
                         reply_markup=inline_calendar(MONTH, YEAR, user_id=message.from_user.id))
    elif message.text == "Добавить":
        bot.reply_to(message, text="Запишите необходимую информацию", reply_markup=remove_keyboard())
        add_mode = 1
    elif message.text == "Да":
        # pass

        ##########  ЕЩЁ НЕМНОГО МОЕГО КОДА
        add_info(message.chat.id, date, information)

        bot.send_message(message.chat.id, text="Информация добавлена, возвращаем вас назад.", reply_markup=gen_info())# хз что делает эта строчка но пусть будет
        ##########


    elif message.text == "Нет":
        bot.send_message(message.chat.id, text="Возвращаем вас назад.", reply_markup=gen_info())

    ###################     ЕЩЕ ОДНА ОТСЕБЯТИНА
    elif message.text == 'Прочитать':
        text_for_write = ''''''
        for i in get_info(date):
            text_for_write += f'\n{i}'

        bot.send_message(message.chat.id, f'{text_for_write}', reply_markup=remove_keyboard())
    ###################

bot.infinity_polling()

if __name__ == "main":
    pass