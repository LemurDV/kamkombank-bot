from telebot import types


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
    bonus_offices = {
        """key - city, value - bonus office"""
        "Казань": [
            "Дополнительный офис в г. Казань, ул. Чистопольская, д.85",
            'Дополнительный офис "Казанский"',
        ],
        "Москва": [
            "Дополнительный офис в г. Москва, ул. Люсиновская, д.29, стр.1",
            "Дополнительный офис в г. Москва, ул. Ярцевская, д.14",
            "Дополнительный офис в г.Москва, ул. Бакунинская, д.50, стр.1",
            "Дополнительный офис в г. Москва, пл. Победы, д.2, стр.1",
            "Дополнительный офис в г. Москва, ул. Тверская, д.6, стр.2",
            "Дополнительный офис в г. Москва, проспект Вернадского, д.33",
            "Дополнительный офис в г. Москва, ул. Бутырская, д.6",
            "Дополнительный офис в г. Москва, ул. Люблинская, д.171",
            "Дополнительный офис в г. Москва, проспект Свободный, 37/18, пом.XIII",
            "Дополнительный офис в г. Москва, Варшавское шоссе, 36",
            "Дополнительный офис в г. Москва, шоссе Каширское, д. 26, корпус 3",
            "Дополнительный офис в г. Москва, Дмитровское шоссе, д. 50, корпус 1",
            "Дополнительный офис в г. Москва, проспект Новоясеневский, д. 32, к. 1",
            "Дополнительный офис в г. Москва, Пресненская набережная, д. 10, стр. 2",
            "Дополнительный офис в г. Москва, ул. Балтийская, д. 4, помещение 1/1",
        ],
        "Санкт-Петербург": [
            "Дополнительный офис в г. Санкт-Петербург, проспект Комендантский, 21",
            "Дополнительный офис в г. Санкт-Петербург, проспект Каменноостровский, 42Б",
            "Дополнительный офис в г. Санкт-Петербург, Московский проспект, 130",
            "Дополнительный офис в г. Санкт-Петербург, ул. Марата, д. 56-58/29",
            "Дополнительный офис в г. Санкт-Петербург, ул. Ивановская, д. 8/77, литера А, помещение 7-H",
            "Дополнительный офис в г. Санкт-Петербург, Новочеркасский проспект, д. 43/17, лит. А, пом. 14-Н",
        ],
        "Набережные Челны": [
            "Головной офис в г. Набережные Челны, ул. Гидростроителей, д.21",
            "Дополнительный офис в г. Набережные Челны, пр. Хасана Туфана, 29Б (14/05Б)",
        ],
        "Альметьевск": [
            'Дополнительный офис  г. Альметьевск, ул. Ленина, 23, "Центр обслуживания населения"',
        ],
        "Ижевск": [
            "Ижевский дополнительный офис"
        ],
    }
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