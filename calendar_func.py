# Python Modules

from calendar import Calendar
import datetime

import telebot.types
# Third-party Modules

from telebot import types
from telebot import TeleBot

today = datetime.date.today().timetuple()
month_names = {1: "Январь", 2: "Февраль", 3: "Март", 4: "Апрель",
               5: "Май", 6: "Июнь", 7: "Июль", 8: "Август",
               9: "Сентябрь", 10: "Октябрь", 11: "Ноябрь", 12: "Декабрь"}

# Глобальные переменные, хранящие данные о дне, месяце и годе

def get_month(month, year):
    """
    Функция, возвращающая массив со всеми днями данного месяца и года
    Если день равен 0, то это значит, что это день прошлого или следующего месяца!
    """
    month_days = list()

    for day in Calendar().itermonthdays(year, month):
        month_days.append(day)

    return month_days


def inline_calendar(m, y, calendar_markup=types.InlineKeyboardMarkup([]), user_id=None):
    """
    Функция, которая возвращает inline-календарь
    :param calendar_markup: хранилище inline-кнопок для календаря
    :param m: месяц
    :param y: год
    """

    print(f"Function inline_calendar() is called")
    calendar_markup = types.InlineKeyboardMarkup([])

    counter = 0
    calendar_buttons_row = list()

    calendar_markup.row(
        types.InlineKeyboardButton(text=str(month_names[m]) + " " + str(y), callback_data="None"))

    for day in get_month(m, y): # Тут нужен месяц и год!
        if day == 0:
            calendar_buttons_row.append(types.InlineKeyboardButton(text=" ", callback_data="None"))
        else:
            calendar_buttons_row.append(types.InlineKeyboardButton(text=day, callback_data=f"{day}"))

        if counter == 7:
            cbr = calendar_buttons_row # Временная замена
            calendar_markup.row(cbr[0], cbr[1], cbr[2], cbr[3], cbr[4], cbr[5], cbr[6])
            calendar_buttons_row.clear()
            counter = 0
        counter += 1

    calendar_markup.row(types.InlineKeyboardButton(text="<<", callback_data="<<"),
                        types.InlineKeyboardButton(text=">>", callback_data=">>"))

    print(user_id, "calendar generated")

    return calendar_markup
