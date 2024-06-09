from telebot import TeleBot
from telebot.types import Message

from db import Database

bot = TeleBot("7235756365:AAFF3JDL3WLliwHP8NSODVgyJugOTvybyFI")
db = Database()


@bot.message_handler(commands=['start'])
def start(message: Message):
    db.insert_user(user_name=message.from_user.username)
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id, text='Привет! Введите ваш номер телефона')
    bot.register_next_step_handler(message, save_user_phone)


def save_user_phone(message: Message):
    db.save_user_phone(phone=int(message.text), user_name=message.from_user.username)


if __name__ == '__main__':
    print('Бот запущен!')
    bot.infinity_polling()
