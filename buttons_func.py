from telebot.types import (KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup,
                           ReplyKeyboardMarkup, ReplyKeyboardRemove)

def remove_keyboard():
    return ReplyKeyboardRemove()


def gen_startbuttons(start_markup=ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)):
    """
    Генерирует кнопки "Пользователь" и "Дежурный"
    :param start_markup:
    :return:
    """
    button1 = KeyboardButton(text="Пользователь")
    button2 = KeyboardButton(text="Дежурный")
    start_markup.row(button1, button2)
    return start_markup


def gen_info(calendar_markup=ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)):
    """
    Генерирует кнопку "Календарь"
    :return:
    """
    button = KeyboardButton(text="Календарь")
    calendar_markup.add(button)
    return calendar_markup


def gen_addread(addread_markup=ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)):
    """
    Генерирует кнопки "Добавить" и "Прочитать"
    ! Только для дежурного !
    :return:
    """
    button1 = KeyboardButton(text="Добавить")
    button2 = KeyboardButton(text="Прочитать")
    addread_markup.row(button1, button2)
    return addread_markup


def gen_yesno(yesno_markup=ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)):
    """
    Генерирует кнопки "Да" и "Нет"
    ! Только для дежурного !
    :return:
    """
    button1 = KeyboardButton(text="Да")
    button2 = KeyboardButton(text="Нет")
    yesno_markup.row(button1, button2)
    return yesno_markup
