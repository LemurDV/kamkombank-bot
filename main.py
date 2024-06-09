import requests
from telebot import TeleBot
from telebot.types import Message

from db import Database
import markups

bot = TeleBot("token")
db = Database()


@bot.message_handler(commands=["start"])
def start(message: Message):
    db.insert_user(user_id=message.from_user.id, user_name=message.from_user.username)
    bot.send_message(chat_id=message.chat.id, text="Отправьте скриншот")
    bot.register_next_step_handler(message, photo_step)


def photo_step(message: Message):
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


def city_choose(message: Message):
    db.save_user_city(user_id=message.from_user.id, city=message.text)

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
        f"Выбрана площадка, на которой был размещен отзыв: {message.text} \nУкажите, пожалуйста, ваше ИМЯ, с которого "
        "был опубликован отзыв."
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
    db.save_user_phone(phone=int(message.text), user_id=message.from_user.id)

    bot.send_message(
        chat_id=message.chat.id,
        text="Данные успешно сохранены",
        reply_markup=markups.markup_end_case(),
    )
    bot.register_next_step_handler(message, final)


def final(message: Message):
    send_user_info()
    cleanup_db(user_id=message.from_user.id)

    # restart
    bot.register_next_step_handler(message, start)


def send_user_info():
    requests.post(url="", json={})


def cleanup_db(user_id: int):
    db.delete_user(user_id=user_id)


if __name__ == '__main__':
    print('Бот запущен!')
    bot.infinity_polling()
