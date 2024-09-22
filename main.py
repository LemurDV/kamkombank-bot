import requests
from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardRemove

from db import Database
import markups
from settings import bonus_offices, bank_codes
import tempfile
import os

bot = TeleBot("{token}")
db = Database()

dialog_active = {}

@bot.message_handler(commands=["start"])
def start(message: Message):
    global dialog_active
    dialog_active[message.chat.id] = True
    db.insert_user(user_id=message.from_user.id, user_name=message.from_user.username)

    bot.send_message(chat_id=message.chat.id, text="Отправьте скриншот отзыва", reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(message, photo_step)


def new_start(message: Message):
    if message.text == "Добавить еще один отзыв на проверку":

        db.insert_user(user_id=message.from_user.id, user_name=message.from_user.username)
        bot.send_message(chat_id=message.chat.id, text="Отправьте скриншот отзыва", reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(message, photo_step)

    elif message.text == "Завершить диалог с ботом":
        global dialog_active
        dialog_active[message.chat.id] = False
        bot.send_message(
            chat_id=message.chat.id,
            text="Диалог завершен. Чтобы начать снова, нажмите /start.",
            reply_markup=markups.make_start_markup()
        )
    else:
        bot.send_message(chat_id=message.chat.id, text="Пожалуйста, выберите одну из кнопок.")
        bot.register_next_step_handler(message, new_start)

def photo_step(message: Message):
    if not message.photo:
        bot.send_message(chat_id=message.chat.id, text="Отправьте скриншот еще раз")
        bot.register_next_step_handler(message, photo_step)
    else:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        db.save_photo(user_id=message.from_user.id, photo=downloaded_file)

        #
        bot.send_message(
            chat_id=message.chat.id,
            text="Выберите город, в котором находится отделение банка:",
            reply_markup=markups.make_city_markup(),
        )
        #
        bot.register_next_step_handler(message, city_choose)


def city_choose(message: Message):
    db.save_user_city(user_id=message.from_user.id, city=message.text)
    if message.text not in bonus_offices:
        bot.send_message(chat_id=message.chat.id, text="Выберите город из указанного списка")
        bot.register_next_step_handler(message, city_choose)
    else:
        #
        bot.send_message(
            chat_id=message.chat.id,
            text="Выберите отделение банка:",
            reply_markup=markups.make_office_markup(city=message.text),
        )
        #
        bot.register_next_step_handler(message, office_choose)


def office_choose(message: Message):
    db.save_user_office(user_id=message.from_user.id, office=message.text)

    #
    bot.send_message(
        chat_id=message.chat.id,
        text="Выберите площадку, на которой был опубликован отзыв:",
        reply_markup=markups.make_recall_place(),
    )
    #
    bot.register_next_step_handler(message, recall_place_choose)


def recall_place_choose(message: Message):
    db.save_recall_place(user_id=message.from_user.id, recall_place=message.text)
    bot.send_message(
        chat_id=message.chat.id,
        text="Укажите, пожалуйста, ваше ИМЯ, с которого был опубликован отзыв.",
        reply_markup=ReplyKeyboardRemove(),
    )
    bot.register_next_step_handler(message, full_name)


def full_name(message: Message):
    db.save_user_full_name(user_id=message.from_user.id, full_name=message.text)
    bot.send_message(
        chat_id=message.chat.id,
        text="Укажите, пожалуйста, номер телефона для совершения перевода через СПБ.",
    )
    bot.register_next_step_handler(message, save_user_phone)


def save_user_phone(message: Message):
    formatted_number = validate_phone(phone=message.text)
    if formatted_number:
        db.save_user_phone(phone=formatted_number, user_id=message.from_user.id)
        bot.send_message(
            chat_id=message.chat.id,
            text="Выберите банк, на который должен поступить платеж:",
            reply_markup=markups.make_user_bank(),
        )
        bot.register_next_step_handler(message, user_bank)
    else:
        bot.edit_message_text(chat_id=message.chat.id, text="s")
        bot.send_message(
            chat_id=message.chat.id,
            text="Не удалось преобразовать номер в нужный формат.",
        )
        bot.register_next_step_handler(message, save_user_phone)


def user_bank(message: Message):
    db.save_user_bank(user_id=message.from_user.id, bank=message.text)

    user = db.get_user(user_id=message.from_user.id)
    text = (
        f"Проверьте, пожалуйста, внимательно указанный номер телефона и банк получателя.\n"
        f"Телефон: {user[8]}\n"
        f"Банк: {user[9]}\n"
        "Всё верно?"
    )

    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markups.button_yes_no())
    bot.register_next_step_handler(message, handle_check_response)

def handle_check_response(message: Message):
    if message.text == "Данные указаны верно, отправить отзыв на проверку":
        send_user_info(user_id=message.from_user.id)
        cleanup_db(user_id=message.from_user.id)

        text = (
            "Данные успешно сохранены. \nСпасибо за Ваши положительные впечатления - Вознаграждение ждет Вас! \n"
            "Выплата будет осуществлена в течение суток после проверки.\n \n"
            "Вы можете оставить отзывы 5 ⭐ на: \n"
            "<a href='https://www.banki.ru/services/responses/response/add/'>Банки.ру</a> и получить сразу <b>200 рублей</b> и еще <b>1800 рублей</b>, когда у отзыва проявится статус <b>ЗАЧТЕНО</b>. "
            "<a href='https://www.banki.ru/services/responses/rules/'>Инструкция</a>, как правильно оставить отзыв на Банки ру. \n"
            "<a href='https://www.google.com/maps/place/%D0%9A%D0%B0%D0%BC%D0%BA%D0%BE%D0%BC%D0%B1%D0%B0%D0%BD%D0%BA/@55.782859,49.126913,17z/data=!4m8!3m7!1s0x415ead0f45c06013:0x63fa2c5c7d3baab1!8m2!3d55.782856!4d49.1294879!9m1!1b1!16s%2Fg%2F1tf46ptz?entry=ttu'>Google Карты</a>  - 50 рублей \n"
            "<a href='https://yandex.ru/maps/org/kamkombank/13276952943/?indoorLevel=1&ll=37.746885%2C55.647179&z=17'>Яндекс Карты</a>  - 50 рублей \n"
            "<a href='https://2gis.ru/spb/branches/70000001066759650'>2ГИС</a> - 50 рублей \n"
            "<a href='https://www.sravni.ru/bank/kamskij-kommercheskij-bank/otzyvy/add/?filterBy=all'>Сравни.ру</a>  - 50 рублей \n"
        )
        bot.send_message(
            chat_id=message.chat.id,
            text=text,
            parse_mode='HTML',
            disable_web_page_preview=True,
            reply_markup=markups.markup_end_case()
        )

        bot.register_next_step_handler(message, new_start)

    elif message.text == "Исправить указанный номер телефона и банк получателя":
        bot.send_message(
            chat_id=message.chat.id,
            text="Пожалуйста, введите номер телефона ещё раз.",
            reply_markup=ReplyKeyboardRemove(),
        )
        bot.register_next_step_handler(message, save_user_phone)
    else:
        bot.send_message(chat_id=message.chat.id, text="Пожалуйста, выберите одну из кнопок.")
        bot.register_next_step_handler(message, handle_check_response)


def validate_phone(phone):
    digits_only = ''.join(filter(str.isdigit, phone))

    # Проверка на длину номера
    if len(digits_only) == 11 and digits_only.startswith('8'):
        # Если номер начинается с 8, заменить на +7
        formatted_number = '+7' + digits_only[1:]
    elif len(digits_only) == 10:
        # Если номер состоит из 10 цифр, добавить +7 в начало
        formatted_number = '+7' + digits_only
    else:
        formatted_number = f"+{digits_only}"

    return formatted_number


def send_user_info(user_id: int):
    user = db.get_user(user_id=user_id)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
        tmp_file.write(user[7])
        tmp_file_path = tmp_file.name

    bank_code = bank_codes.get(user[9])

    requests.post(
        url="http://localhost:8022/lead",
        # url="https://api.evoreview.ru/lead",
        data={
            "user_name": user[2],
            "full_name": user[3],
            "city": user[4],
            "office": user[5],
            "recall_place": user[6],
            "phone": user[8],
            "bank_code": bank_code
        },
        files={
            "image_bytes": open(tmp_file_path, 'rb')
        }
    )
    os.remove(tmp_file_path)


def cleanup_db(user_id: int):
    db.delete_user(user_id=user_id)


if __name__ == '__main__':
    print('Бот запущен!')
    bot.infinity_polling()
