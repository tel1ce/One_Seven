from calendar import Calendar
import datetime

import sqlite3
from test import *

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

# def add_user_n(tgtoken):
#
#     us_id = str(tgtoken)
#     ishead = 0
#     cur = cursor.connection("db_mvp.db")
#     cur.execute(
#         f'INSERT INTO USERS(tgtoken, isheadman) VALUES(?, ?)', (us_id, ishead)
#     )
#     connect.commit()


def get_calendar(MONTH, YEAR):
    return Calendar().itermonthdays(YEAR, MONTH)
API_TOKEN = "6553729037:AAH_RXxoOp6TsRdI7Se6OtOJ3oHyGLGAbZM"

bot = TeleBot(API_TOKEN)

# Роли пользователя бота
roles = ["Пользователь", "Дежурный"]
kbd_user = tbt.types.KeyboardButton(text=roles[0])
kbd_mod = tbt.types.KeyboardButton(text=roles[1])
kbd_roles = tbt.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(kbd_user, kbd_mod)

# Функция info
info_button = tbt.types.KeyboardButton(text="Календарь")
info_markup = tbt.types.ReplyKeyboardMarkup(resize_keyboard=True).add(info_button)
info_markup2 = tbt.types.ReplyKeyboardMarkup(resize_keyboard=True).add(info_button)

# Функции добавления и чтения
add_info_button = tbt.types.KeyboardButton(text="Добавить")
read_info_button = tbt.types.KeyboardButton(text="Прочитать")
add_read_markup = tbt.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(add_info_button, read_info_button)

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
calendar_markup = tbt.types.InlineKeyboardMarkup()
list_calendar_buttons = list()
today = datetime.date.today().timetuple()
MONTH = today[1]
DAY = today[2]
YEAR = today[0]

month_names = {1:"Январь", 2:"Февраль", 3:"Март", 4:"Апрель",
               5:"Май", 6:"Июнь", 7:"Июль", 8:"Август",
               9:"Сентябрь", 10:"Октябрь", 11:"Ноябрь", 12:"Декабрь"}

def gen_calendar():
    global calendar_markup
    calendar_markup = tbt.types.InlineKeyboardMarkup(keyboard=[])
    print("gen_calendar() is called")
    c = 1
    print(DAY, MONTH, YEAR)
    calendar_markup.row(tbt.types.InlineKeyboardButton(text=str(month_names[MONTH])+" "+str(YEAR), callback_data=" "))
    for day in get_calendar(MONTH, YEAR):
        if day == 0:
            day = " "
        list_calendar_buttons.append(tbt.types.InlineKeyboardButton(text=day, callback_data=str(day)))
        if c == 7:
            c = 0
            lcb = list_calendar_buttons
            calendar_markup.row(lcb[0], lcb[1], lcb[2], lcb[3], lcb[4], lcb[5], lcb[6])
            list_calendar_buttons.clear()
        c += 1
    calendar_markup.row(tbt.types.InlineKeyboardButton(text="<<", callback_data="<<"),
                        tbt.types.InlineKeyboardButton(text=">>", callback_data=">>"))


# def role_dependence():
#     global add_read_markup
#     if role == "user":
#         pass
#     elif role == "mod":
#         add_read_markup.row(add_info_button, read_info_button)
#         print('add_read_markup == ', add_read_markup)


@bot.message_handler(commands=["start", "help"])
def start_message(message):

    calendar_markup = tbt.types.InlineKeyboardMarkup(keyboard=[])
    bot.reply_to(message, "Это OneSeven_Bot, бот для удобного поиска информации по классу в школе.\n"
                                "Для начала выберите свою роль", reply_markup=kbd_roles)


    ######################          РАБОТАЕТ+
    if check_user(message.from_user.id) == 1:
        add_user(str(message.from_user.id), 0)


@bot.message_handler(commands=["Календарь"])
def mod_cmd(message):
    global calendar_markup
    gen_calendar()
    print(calendar_markup)
    bot.send_message(message.chat.id, text="Выберите день из календаря", reply_markup=calendar_markup)
    calendar_markup = tbt.types.InlineKeyboardMarkup(keyboard=[])


@bot.callback_query_handler(lambda call: True)
def answer(call):
    global calendar_markup
    global DAY
    global MONTH
    global YEAR
    global date
    m = MONTH
    d = call.data
    print(call)
    if (len(call.data) == 1) and (call.data != " "):
        d = int("0" + call.data)
    if len(str(MONTH)) == 1:
        m = int("0" + str(MONTH))
    date = f"{d}.{m}.{YEAR}"
    try:
        # role_dependence()
        if int(call.data) in range(32):
            if role == "user":
                bot.send_message(call.message.chat.id,
                                 text=f"Выбрана дата {d}.{m}.{YEAR}. Отправляем информацию:")# Все работает но может есть смысл сменить на date, убрал , reply_markup=add_read_markup

                ########################        МОЯ САМОДЕЯТЕЛЬНОСТЬ, ВНИМАТЕЛЬНО ОСМОТРЕТЬ
                # all_info = get_info(date)
                text_for_write = ''''''

                for i in get_info(date):
                    text_for_write += f'\n{i}'

                bot.send_message(call.message.chat.id, f'{text_for_write}')
                ######################## ВРОДЕ РАБОТАЕТ

            elif role == "mod":
                #########################################   Тут был косяк     v   из-за чего неправильно выводилась дата (кажется сейчас все нормально)
                bot.send_message(call.message.chat.id, text=f"Выбрана дата {date}. Что делать с информацией?", reply_markup=add_read_markup)
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
        gen_calendar()
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=calendar_markup)
    elif call.data == "<<":
        if MONTH != 1:
            DAY = 1
            MONTH -= 1
        else:
            DAY = 1
            MONTH = 12
            YEAR -= 1
        gen_calendar()
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=calendar_markup)


@bot.message_handler(content_types=['text'])
def user_text(message):
    global role
    global information
    global add_mode
    global date ######  Это надо (на будущее если я не ошибаюсь можно написать: global role, information, add_mode, date) выглядит лучше(наверное, а может и нет)
    if message.text == "Пользователь":
        role = "user"
        bot.send_message(message.chat.id, text="Теперь вы пользователь.\nНажмите на кнопку календарь, чтобы выбрать дату дня, информацию которого вы хотите получить", reply_markup=info_markup)
    if add_mode == 1:
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
    elif message.text == "Дежурный":
        role = "mod"
        bot.send_message(message.chat.id, text="Теперь вы дежурный.\nНажмите на кнопку календарь, чтобы выбрать дату дня, на который вы хотите добавить/изменить информацию", reply_markup=info_markup)
    elif message.text == "Календарь":
        gen_calendar()
        print(calendar_markup)
        bot.send_message(message.chat.id, text="Выберите день из календаря", reply_markup=calendar_markup)
    elif message.text == "Добавить":
        bot.reply_to(message, text="Запишите необходимую информацию")
        add_mode = 1
    elif message.text == "Да":
        # pass

        ##########  ЕЩЁ НЕМНОГО МОЕГО КОДА
        add_info(message.chat.id, date, information)

        bot.send_message(message.chat.id, text="Информация добвалена ,возвращаем вас назад.", reply_markup=info_markup)# хз что делает эта строчка но пусть будет
        ##########


    elif message.text == "Нет":
        bot.send_message(message.chat.id, text="Возвращаем вас назад.", reply_markup=info_markup)

    ###################     ЕЩЕ ОДНА ОТСЕБЯТИНА
    elif message.text == 'Прочитать':
        text_for_write = ''''''

        for i in get_info(date):
            text_for_write += f'\n{i}'

        bot.send_message(message.chat.id, f'{text_for_write}')
    ###################

bot.infinity_polling()

if __name__ == "main":
    pass