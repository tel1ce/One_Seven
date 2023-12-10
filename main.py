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
            CREATE TABLE IF NOT EXISTS PRIVATE_INFO(
                tgtoken STR,
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

feedback_button = tbt.types.KeyboardButton(text="Обратная связь")


list_commands = []
back_button = tbt.types.KeyboardButton(text="Назад")


# Функция info
info_button = tbt.types.KeyboardButton(text="Календарь")
info_markup = tbt.types.ReplyKeyboardMarkup(resize_keyboard=True).add(info_button)
info_markup.add(feedback_button)
info_markup.add(back_button)


refactor_private_info = tbt.types.KeyboardButton(text="Изменить приватную информацию")
refactor_public_info = tbt.types.KeyboardButton(text="Изменить общую информацию")

# Функции добавления и чтения
add_info_button = tbt.types.KeyboardButton(text="Добавить")
add_private_info_button = tbt.types.KeyboardButton(text="Добавить приватную информацию")
read_info_button = tbt.types.KeyboardButton(text="Прочитать")
add_read_markup = tbt.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(add_private_info_button)
add_read_markup.add(add_info_button, read_info_button)
add_read_markup.add(refactor_public_info)
add_read_markup.add(refactor_private_info)
add_read_markup.add(back_button)


delete_button = tbt.types.KeyboardButton(text="Удалить")
delete_markup = tbt.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(delete_button)
delete_markup.add(back_button)


add_read_markup_user = tbt.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(add_private_info_button)
add_read_markup_user.add(read_info_button)
add_read_markup_user.add(refactor_private_info)


add_mode = 0 # Находится ли пользователь в состоянии добавления информации? 0 или 1
add_private_info_mode = 0
refactor_private_info_mode = 0
refactor_public_info_mode = 0
type_add = ''

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

def gen_calendar(token, type='FIRST'):
    global calendar_markup, today, MONTH, YEAR

    if type == 'FIRST':
        MONTH = today[1]
        DAY = today[2]
        YEAR = today[0]

    calendar_markup = tbt.types.InlineKeyboardMarkup(keyboard=[])
    c = 1
    calendar_markup.row(tbt.types.InlineKeyboardButton(text=str(month_names[MONTH])+" "+str(YEAR), callback_data=" "))
    for day in get_calendar(MONTH, YEAR):
        if day == 0:
            day = " "

        ch_date = str(f'{day}.{MONTH}.{YEAR}')
        app_part = ''
        if len(ch_date) >= 8:
            if is_have_info(token, ch_date) == True:
                app_part = '*'

        list_calendar_buttons.append(tbt.types.InlineKeyboardButton(text=f'{day}{app_part}', callback_data=str(day)))
        if c == 7:
            c = 0
            lcb = list_calendar_buttons
            calendar_markup.row(lcb[0], lcb[1], lcb[2], lcb[3], lcb[4], lcb[5], lcb[6])
            list_calendar_buttons.clear()
        c += 1
    calendar_markup.row(tbt.types.InlineKeyboardButton(text="<<", callback_data="<<"), tbt.types.InlineKeyboardButton(text=">>", callback_data=">>"))

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

#

@bot.callback_query_handler(lambda call: True)
def answer(call):
    global calendar_markup
    global DAY
    global MONTH
    global YEAR
    global date, list_commands
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
                n = bot.send_message(call.message.chat.id, text=f"Выбрана дата {date}. Что делать с информацией?", reply_markup=add_read_markup_user)
                list_commands.append(['выбрана дата', n.message_id])

            elif role == "mod":
                n = bot.send_message(call.message.chat.id, text=f"Выбрана дата {date}. Что делать с информацией?", reply_markup=add_read_markup)
                list_commands.append(['выбрана дата', n.message_id])


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
        gen_calendar(call.message.chat.id, type='NEXT')
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=calendar_markup)
    elif call.data == "<<":
        if MONTH != 1:
            DAY = 1
            MONTH -= 1
        else:
            DAY = 1
            MONTH = 12
            YEAR -= 1
        gen_calendar(call.message.chat.id, type='NEXT')
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=calendar_markup)

@bot.message_handler(content_types=['text'])
def user_text(message):
    global role
    global information
    global add_mode, add_private_info_mode, type_add
    global date, refactor_private_info_mode, refactor_public_info_mode, list_commands


    if message.text == 'Назад':
        if len(list_commands) != 0:
            print(list_commands)
            if list_commands[-1][0] == 'выбрана дата':
                bot.delete_message(message.chat.id, list_commands[-1][-1])
                bot.delete_message(message.chat.id, list_commands[-2][-1])
                list_commands.pop(-1)
                list_commands.pop(-1)
                gen_calendar(message.chat.id)
                n = bot.send_message(message.chat.id, text="Выберите день из календаря", reply_markup=calendar_markup)
                list_commands.append(['календарь', n.message_id])

            elif list_commands[-1][0] == 'изменить приватную информацию':
                bot.delete_message(message.chat.id, list_commands[-1][-1])
                list_commands.pop(-1)
                n = bot.send_message(message.chat.id, text=f"Выбрана дата {date}. Что делать с информацией?", reply_markup=add_read_markup)
                list_commands.append(['выбрана дата', n.message_id])

            elif list_commands[-1][0] == 'изменить общую информацию':
                bot.delete_message(message.chat.id, list_commands[-1][-1])
                list_commands.pop(-1)
                n = bot.send_message(message.chat.id, text=f"Выбрана дата {date}. Что делать с информацией?", reply_markup=add_read_markup)
                list_commands.append(['выбрана дата', n.message_id])

            elif list_commands[-1][0] == 'добавить':
                bot.delete_message(message.chat.id, list_commands[-1][-1])
                list_commands.pop(-1)
                n = bot.send_message(message.chat.id, text=f"Выбрана дата {date}. Что делать с информацией?", reply_markup=add_read_markup)
                list_commands.append(['выбрана дата', n.message_id])

            elif list_commands[-1][0] == 'добавить приватную информацию':
                bot.delete_message(message.chat.id, list_commands[-1][-1])
                list_commands.pop(-1)
                n = bot.send_message(message.chat.id, text=f"Выбрана дата {date}. Что делать с информацией?", reply_markup=add_read_markup)
                list_commands.append(['выбрана дата', n.message_id])

            elif list_commands[-1][0] == 'прочитать':
                for i in list_commands[-1][-1]:
                    bot.delete_message(message.chat.id, i)
                list_commands.pop(-1)
                n = bot.send_message(message.chat.id, text=f"Выбрана дата {date}. Что делать с информацией?", reply_markup=add_read_markup)
                list_commands.append(['выбрана дата', n.message_id])

            elif list_commands[-1][0] == 'обратная связь':
                bot.delete_message(message.chat.id, list_commands[-1][-1])
                list_commands.pop(-1)
            print(list_commands)
        else:
            bot.send_message(message.chat.id, 'Невозможно вернуться на предыдущий шаг', reply_markup=info_markup)


    if str(message.text).lower() == "календарь":
        if check_isheadman(message.chat.id) == 1:
            role = 'mod'
        else:
            role = 'user'
        gen_calendar(message.chat.id)

        n = bot.send_message(message.chat.id, text="Выберите день из календаря", reply_markup=calendar_markup)
        list_commands.append( ['календарь', n.message_id] )


    elif message.text == 'Изменить приватную информацию':
        text_for_write_2 = f'''{date} Текущая приватная информация:\n'''
        if get_private_info(message.chat.id, date) != False:
            for i in get_private_info(message.chat.id, date):
                text_for_write_2 += f'\n{i}'
            n = bot.send_message(message.chat.id, f'{text_for_write_2}\n\n*Если хотите удалить информацию, воспользуйтесь соответствующей кнопкой*\nВведите новую приватную информацию:', reply_markup=delete_markup)
            refactor_private_info_mode = 1
            list_commands.append( ['изменить приватную информацию', n.message_id] )

        else:
            bot.send_message(message.chat.id, f'На эту дату еще нет приватной информации', reply_markup=info_markup)


    elif message.text == 'Изменить общую информацию':
        text_for_write_2 = f'''{date} Текущая информация\n'''
        if get_info(date) != False:
            for i in get_info(date):
                text_for_write_2 += f'\n{i}'
            bot.send_message(message.chat.id, f'{text_for_write_2}')

            n = bot.send_message(message.chat.id, f'*Если хотите удалить информацию, воспользуйтесь соответствующей кнопкой*\nВведите новую информацию:', reply_markup=delete_markup)
            refactor_public_info_mode = 1
            list_commands.append(['изменить общую информацию', n.message_id])

        else:
            bot.send_message(message.chat.id, f'На эту дату еще нет информации', reply_markup=info_markup)


    elif message.text == 'Удалить':
        if refactor_public_info_mode == 1:
            delete_info(message.chat.id, date)
            bot.send_message(message.chat.id, f'Информация успешно удалена', reply_markup=info_markup)
            refactor_public_info_mode = 0
        elif refactor_private_info_mode == 1:
            delete_private_info(message.chat.id, date)
            bot.send_message(message.chat.id, f'Информация успешно удалена', reply_markup=info_markup)
            refactor_private_info_mode = 0


    elif message.text == "Добавить":
        if check_isheadman(message.chat.id) == 1:
            role = 'mod'
            if date != '':
                n = bot.reply_to(message, text="Запишите необходимую информацию")
                list_commands.append(['добавить', n.message_id])

                add_mode = 1
            else:
                bot.send_message(message.chat.id, text='Вы еще не выбрали дату, сделайте это через команду календарь', reply_markup=info_markup)
        else:
            role = 'user'
            bot.send_message(message.chat.id, text='У вас нат прав на такие команды', reply_markup=info_markup)


    elif message.text == "Да":
        if information != '':

            if type_add == 'private':
                add_private_info(message.chat.id, date, information)
                bot.send_message(message.chat.id, text="Приватная информация добавлена\nДля дальнейших действий воспользуйтесь командой календарь", reply_markup=info_markup)
            elif type_add == 'public':
                add_info(message.chat.id, date, information)
                bot.send_message(message.chat.id, text="Информация добавлена\nДля дальнейших действий воспользуйтесь командой календарь", reply_markup=info_markup)
            elif type_add == 'refactor_private':
                change_private_info(message.chat.id, date, information)
                bot.send_message(message.chat.id,text="Приватная информация изменена\nДля дальнейших действий воспользуйтесь командой календарь", reply_markup=info_markup)
            elif type_add == 'refactor_public':
                change_public_info(message.chat.id, date, information)
                bot.send_message(message.chat.id,text="Информация изменена\nДля дальнейших действий воспользуйтесь командой календарь", reply_markup=info_markup)

            information = ''
            date = ''
            add_mode = 0
            add_private_info_mode = 0
            type_add = ''
            list_commands = []
        else:
            bot.send_message(message.chat.id, text="Сначала необходимо внести информацию, воспользуйтесь командой календарь", reply_markup=info_markup)


    elif message.text == "Нет":
        if information != '':
            bot.send_message(message.chat.id, text="Возвращаем вас назад.", reply_markup=info_markup)
            information = ''
            date = ''
            add_mode = 0
            add_private_info_mode = 0
            list_commands = []
        else:
            bot.send_message(message.chat.id, text="Нечего отменять - вы еще не вносили информацию, воспользуйтесь командой календарь", reply_markup=info_markup)


    elif message.text == 'Прочитать':
        list_to_command = []
        back_mode = ''
        if date != '':
            text_for_write_1 = f'''{date} Общая информация\n'''
            if get_info(date) != False:
                for i in get_info(date):
                    text_for_write_1 += f'\n{i}'
                n1 = bot.send_message(message.chat.id, f'{text_for_write_1}', reply_markup=info_markup)
                list_to_command.append(n1.message_id)

            text_for_write_2 = f'''{date} Приватная информация\n'''
            if get_private_info(message.chat.id, date) != False:
                for i in get_private_info(message.chat.id, date):
                    text_for_write_2 += f'\n{i}'
                n2 = bot.send_message(message.chat.id, f'{text_for_write_2}', reply_markup=info_markup)
                list_to_command.append(n2.message_id)

            if get_info(date) == False and get_private_info(message.chat.id, date) == False:
                n3 = bot.send_message(message.chat.id, f'На эту дату нет информации', reply_markup=info_markup)
                list_to_command.append(n3.message_id)
                date = ''

            list_commands.append(['прочитать', list_to_command])

        else:
            bot.send_message(message.chat.id, text='Сначала необходимо выбрать дату, воспользуйтесь командой календарь', reply_markup=info_markup)


    elif message.text == "Обратная связь":
        n = bot.reply_to(message, text="Вот ссылка на гугл-форму:\nhttps://forms.gle/FerrU3z9sWivUWfQ7")
        list_commands.append( ['обратная связь', n.message_id] )


    elif message.text == 'Добавить приватную информацию':
        if date != '':
            n = bot.reply_to(message, text="Запишите приватную информацию")
            add_private_info_mode = 1
            list_commands.append( ['добавить приватную информацию', n.message_id] )
        else:
            bot.send_message(message.chat.id, text='Вы еще не выбрали дату, сделайте это через команду календарь', reply_markup=info_markup)


    elif add_mode == 1:
        if str(message.text).lower() not in ['да', 'нет', 'календарь', 'добавить', 'прочитать', 'добавить приватную информацию', 'назад', 'удалить']:
            information = message.text
            bot.reply_to(message, text=f"На {date} вы добавили информацию: \n{information}\nВы уверены?", reply_markup=add_final_markup)
            add_mode = 0
            type_add = 'public'


    elif refactor_private_info_mode == 1:
        if str(message.text).lower() not in ['да', 'нет', 'календарь', 'добавить', 'прочитать', 'добавить приватную информацию', 'назад', 'удалить']:
            information = message.text
            bot.reply_to(message, text=f"На {date} вы хотите поменять информацию на:\n{information}\nВы уверены?", reply_markup=add_final_markup)
            refactor_private_info_mode = 0
            type_add = 'refactor_private'


    elif refactor_public_info_mode == 1:
        if str(message.text).lower() not in ['да', 'нет', 'календарь', 'добавить', 'прочитать', 'добавить приватную информацию', 'назад', 'удалить']:
            information = message.text
            bot.reply_to(message, text=f"На {date} вы хотите поменять информацию на:\n{information}\nВы уверены?", reply_markup=add_final_markup)
            refactor_public_info_mode = 0
            type_add = 'refactor_public'


    elif add_private_info_mode == 1:
        if str(message.text).lower() not in ['да', 'нет', 'календарь', 'добавить', 'прочитать', 'добавить приватную информацию', 'назад', 'удалить']:
            information = message.text
            bot.reply_to(message, text=f"На {date} вы добавили информацию:\n{information}\nВы уверены?", reply_markup=add_final_markup)
            add_private_info_mode = 0
            type_add = 'private'

if __name__ == '__main__':
    while True:
        try:
            bot.polling(non_stop=True)
        except Exception as e:
            time.sleep(3)