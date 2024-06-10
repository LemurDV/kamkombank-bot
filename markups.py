from telebot import types

from settings import bonus_offices


def make_city_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Москва")
    button2 = types.KeyboardButton("Санкт-Петербург")
    button3 = types.KeyboardButton("Казань")
    button4 = types.KeyboardButton("Набережные Челны")
    button5 = types.KeyboardButton("Ижевск")
    button5 = types.KeyboardButton("Альметьевск")
    markup.add(button1, button2, button3, button4, button5)
    return markup


def make_office_markup(city: str):
    offices = bonus_offices.get(city)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for office in offices:
        markup.add(types.KeyboardButton(office))
    return markup


def make_recall_place():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Банки.ру ")
    button2 = types.KeyboardButton("Google Карты ")
    button3 = types.KeyboardButton("Яндекс. Карты")
    button4 = types.KeyboardButton("2ГИС")
    button5 = types.KeyboardButton("Сравни.ру")
    button6 = types.KeyboardButton("Bankiros")
    markup.add(button1, button2, button3, button4, button5, button6)
    return markup


def markup_end_case():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton(text="Добавить еще один отзыв на проверку")
    button2 = types.KeyboardButton("Завершить диалог с ботом")
    markup.add(button1, button2)
    return markup
