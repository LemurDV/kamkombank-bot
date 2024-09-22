from telebot import types

from settings import bonus_offices


def make_city_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Москва")
    button2 = types.KeyboardButton("Санкт-Петербург")
    button3 = types.KeyboardButton("Казань")
    button4 = types.KeyboardButton("Набережные Челны")
    button5 = types.KeyboardButton("Ижевск")
    button6 = types.KeyboardButton("Альметьевск")
    markup.add(button1, button2, button3, button4, button5, button6)
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


def make_user_bank():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # 100000000111
    button1 = types.KeyboardButton("Сбербанк")
    # 100000000005
    button2 = types.KeyboardButton("ВТБ")
    # 100000000008
    button3 = types.KeyboardButton("Альфа Банк")
    # 100000000004
    button4 = types.KeyboardButton("Т-Банк")
    # 100000000015
    button5 = types.KeyboardButton("Банк ФК Открытие")
    # 100000000006
    button6 = types.KeyboardButton("Ак Барс Банк")
    # 100000000001
    button7 = types.KeyboardButton("Газпромбанк")
    # 100000000007
    button8 = types.KeyboardButton("Райффайзен Банк")
    # 100000000012
    button9 = types.KeyboardButton("Росбанк")
    # 100000000013
    button10 = types.KeyboardButton("Совкомбанк")
    # 100000000030
    button11 = types.KeyboardButton("ЮниКредит Банк")
    # 100000000020
    button12 = types.KeyboardButton("Россельхозбанк")
    # 100000000016
    button13 = types.KeyboardButton("Почта Банк")
    # 100000000025
    button14 = types.KeyboardButton("МКБ (Московский кредитный банк)")
    # 100000000014
    button15 = types.KeyboardButton("Банк Русский Стандарт")
    # 100000000027
    button16 = types.KeyboardButton("Кредит Европа Банк")
    # 100000000024
    button17 = types.KeyboardButton("Хоум Кредит Банк (Хоум Банк)")
    # 100000000289
    button18 = types.KeyboardButton("МТС Деньги (ЭКСИ Банк)")
    # 100000000273
    button19 = types.KeyboardButton("Озон Банк (Ozon)")
    # 100000000259
    button20 = types.KeyboardButton("Wildberries (Вайлдберриз Банк)")
    # 100000000045
    button21 = types.KeyboardButton("Банк ЗЕНИТ")
    markup.add(button1, button2, button3, button4, button5, button6,
               button7, button8, button9, button10, button11, button12,
               button13, button14, button15, button16, button17, button18,
               button19, button20, button21)
    return markup

def make_button_false():
    markup = types.ReplyKeyboardMarkup(selective=False)
    return markup


def button_yes_no():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Данные указаны верно, отправить отзыв на проверку")
    button2 = types.KeyboardButton("Исправить указанный номер телефона и банк получателя")
    markup.add(button1, button2)
    return markup

def make_start_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("/start")
    markup.add(button)
    return markup

def markup_end_case():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton(text="Добавить еще один отзыв на проверку")
    button2 = types.KeyboardButton(text="Завершить диалог с ботом")
    markup.add(button1, button2)
    return markup


def some():
    markup = types.ReplyKeyboardRemove(selective=False)