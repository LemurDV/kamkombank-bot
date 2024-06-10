import requests
from telebot import TeleBot
from telebot.types import Message

from db import Database
import markups
from settings import bonus_offices

bot = TeleBot("token")
db = Database()


@bot.message_handler(commands=["start"])
def start(message: Message):
    db.insert_user(user_id=message.from_user.id, user_name=message.from_user.username)
    bot.send_message(chat_id=message.chat.id, text="Отправьте скриншот")
    bot.register_next_step_handler(message, photo_step)


def photo_step(message: Message):
    db.insert_user(user_id=message.from_user.id, user_name=message.from_user.username)
    if message.photo:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        db.save_photo(user_id=message.from_user.id, photo=str(downloaded_file))

        #
        bot.send_message(
            chat_id=message.chat.id,
            text="Выберите город, в котором находится отделение банка.",
            reply_markup=markups.make_city_markup(),
        )
        #
        bot.register_next_step_handler(message, city_choose)
    else:
        bot.send_message(chat_id=message.chat.id, text="Отправьте скриншот еще раз")
        bot.register_next_step_handler(message, photo_step)


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
        text=(
            f"Выбрана площадка, на которой был размещен отзыв: {message.text} \nУкажите, пожалуйста, ваше ИМЯ, "
            f"с которого был опубликован отзыв."
        ),
    )
    bot.register_next_step_handler(message, full_name)


def full_name(message: Message):
    db.save_user_full_name(user_id=message.from_user.id, full_name=message.text)
    bot.send_message(
        chat_id=message.chat.id,
        text="Данные сохранены.\nПросим предоставить номер телефона для пополнения баланса.",
    )
    bot.register_next_step_handler(message, save_user_phone)


def save_user_phone(message: Message):
    formatted_number = validate_phone(phone=message.text)
    if formatted_number:
        db.save_user_phone(phone=formatted_number, user_id=message.from_user.id)
        bot.send_message(
            chat_id=message.chat.id,
            text="Данные успешно сохранены",
            reply_markup=markups.markup_end_case(),
        )
        bot.register_next_step_handler(message, final)
    else:
        bot.edit_message_text(chat_id=message.chat.id, text="s")
        bot.send_message(
            chat_id=message.chat.id,
            text="Не удалось преобразовать номер в нужный формат.",
        )
        bot.register_next_step_handler(message, save_user_phone)


def validate_phone(phone):
    digits_only = ''.join(filter(str.isdigit, phone))

    # Проверка на длину номера
    if len(digits_only) == 11 and digits_only.startswith('8'):
        # Если номер начинается с 8, заменить на +7
        formatted_number = f"+7{digits_only[1:]}"
    elif len(digits_only) == 10:
        # Если номер состоит из 10 цифр, добавить +7 в начало
        formatted_number = f"+7{digits_only}"
    else:
        formatted_number = None

    return formatted_number


def final(message: Message):
    send_user_info(user_id=message.from_user.id)
    db.delete_user(user_id=message.from_user.id)
    # restart
    bot.register_next_step_handler(message, start)


def send_user_info(user_id: int):
    user = db.get_user(user_id=user_id)
    requests.post(
        url="",
        json={
            "user_name": user[2],
            "full_name": user[3],
            "city": user[4],
            "office": user[5],
            "recall_place": user[6],
            "image_bytes": user[7],
            "phone": user[8],

        },
    )


if __name__ == '__main__':
    print('Бот запущен!')
    bot.infinity_polling()
