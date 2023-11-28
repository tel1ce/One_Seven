import time
from calendar import Calendar
import datetime
from DB_FUNC import *
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

def get_calendar(MONTH, YEAR):
    return Calendar().itermonthdays(YEAR, MONTH)

TOKEN = ''
with open('TOKEN.txt', 'r') as x:
    TOKEN = x.readline()
API_TOKEN = f"{TOKEN}"

bot = TeleBot(API_TOKEN)

# Функция info
info_button = tbt.types.KeyboardButton(text="Календарь")
info_markup = tbt.types.ReplyKeyboardMarkup(resize_keyboard=True).add(info_button)
# info_markup2 = tbt.types.ReplyKeyboardMarkup(resize_keyboard=True).add(info_button)

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
    c = 1
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

@bot.message_handler(commands=["start", "help"])
def start_message(message):
    global role
    if check_user(message.from_user.id) == 1:
        add_user(str(message.from_user.id), 0)
        role = 'user'

        bot.send_message(message.chat.id, text='Добро пожаловать, текущая роль: пользователь\nВыберите дату для получения информации через команду календарь', reply_markup=info_markup)
    elif check_isheadman(message.from_user.id) == 0:
        role = 'user'
        bot.send_message(message.chat.id, text='С возвращением, текущая роль: пользователь\nВыберите дату через команду календарь', reply_markup=info_markup)
    elif check_isheadman(message.from_user.id) == 1:
        role = 'mod'
        bot.send_message(message.chat.id, text='С возвращением, текущая роль: дежурный\nВыберите дату через команду календарь', reply_markup=info_markup)

@bot.message_handler(commands=["Календарь"])
def mod_cmd(message):
    global calendar_markup, role
    if check_isheadman(message.chat.id) == 1:
        role = 'mod'
    else:
        role = 'user'
    gen_calendar()
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
    if (len(call.data) == 1) and (call.data != " "):
        d = int("0" + call.data)
    if len(str(MONTH)) == 1:
        m = int("0" + str(MONTH))
    date = f"{d}.{m}.{YEAR}"
    try:
        if int(call.data) in range(32):
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=None)
            if check_isheadman(call.message.chat.id) == 1:
                role = 'mod'
            else:
                role = 'user'
            if role == "user":
                bot.send_message(call.message.chat.id, text=f"Выбрана дата {d}.{m}.{YEAR}. Отправляем информацию:")# Все работает но может есть смысл сменить на date, убрал , reply_markup=add_read_markup

                text_for_write = ''''''

                if get_info(date) != False:
                    for i in get_info(date):
                        text_for_write += f'\n{i}'

                    bot.send_message(call.message.chat.id, f'{text_for_write}')
                    bot.send_message(call.message.chat.id, text='Для получения новой информации вы всегда можете снова выбрать команду календарь')
                else:
                    bot.send_message(call.message.chat.id, text='На эту дату нет информации')

            elif role == "mod":
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
    global date
    # if message.text == "Пользователь":
    #     role = "user"
    #     bot.send_message(message.chat.id, text="Теперь вы пользователь.\nНажмите на кнопку календарь, чтобы выбрать дату дня, информацию которого вы хотите получить", reply_markup=info_markup)
    if add_mode == 1:

        if str(message.text).lower() not in ['да', 'нет', 'календарь', 'добавить', 'прочитать']:
            information = message.text

            bot.reply_to(message, text=f"Вы добавили информацию: {information}. \nВы уверены?", reply_markup=add_final_markup)

            add_mode = 0

    elif str(message.text).lower() == "календарь":
        if check_isheadman(message.chat.id) == 1:
            role = 'mod'
        else:
            role = 'user'
        gen_calendar()
        bot.send_message(message.chat.id, text="Выберите день из календаря", reply_markup=calendar_markup)


    elif message.text == "Добавить":
        if check_isheadman(message.chat.id) == 1:
            role = 'mod'
            if date != '':
                bot.reply_to(message, text="Запишите необходимую информацию")

                add_mode = 1
            else:
                bot.send_message(message.chat.id, text='Вы еще не выбрали дату, сделайте это через команду календарь', reply_markup=info_markup)
        else:
            role = 'user'
            bot.send_message(message.chat.id, text='У вас нат прав на такие команды', reply_markup=info_markup)


    elif message.text == "Да":
        if check_isheadman(message.chat.id) == 1:
            role = 'mod'
            if information != '':
                add_info(message.chat.id, date, information)
                bot.send_message(message.chat.id, text="Информация добавлена\nДля дальнейших действий воспользуйтесь командой календарь", reply_markup=info_markup)
                information = ''
                date = ''
            else:
                bot.send_message(message.chat.id, text="Сначала необходимо внести информацию, воспользуйтесь командой календарь", reply_markup=info_markup)

        else:
            role = 'user'
            bot.send_message(message.chat.id, text='У вас нат прав на такие команды', reply_markup=info_markup)


    elif message.text == "Нет":
        if check_isheadman(message.chat.id) == 1:
            role = 'mod'
            if information != '':
                bot.send_message(message.chat.id, text="Возвращаем вас назад.", reply_markup=info_markup)
                information = ''
                date = ''
            else:
                bot.send_message(message.chat.id, text="Нечего отменять - вы еще не вносили информацию, воспользуйтесь командой календарь", reply_markup=info_markup)

        else:
            role = 'user'
            bot.send_message(message.chat.id, text='У вас нат прав на такие команды', reply_markup=info_markup)


    elif message.text == 'Прочитать':
        if check_isheadman(message.chat.id) == 1:
            role = 'mod'
            if date != '':
                text_for_write = ''''''
                if get_info(date) != False:
                    for i in get_info(date):
                        text_for_write += f'\n{i}'
                    bot.send_message(message.chat.id, f'{text_for_write}', reply_markup=info_markup)
                else:
                    bot.send_message(message.chat.id, f'На эту дату нет информации', reply_markup=info_markup)
                    date = ''
            else:
                bot.send_message(message.chat.id, text='Сначала необходимо выбрать дату, воспользуйтесь командой календарь', reply_markup=info_markup)

        else:
            role = 'user'
            bot.send_message(message.chat.id, 'Вы пользователь и вам не нужна эта команда, выберите дату через календарь и вы получите информацию')

if __name__ == '__main__':
    while True:
        try:
            bot.polling(non_stop=True)
        except Exception as e:
            time.sleep(3)