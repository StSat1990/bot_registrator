import telebot
import buttons
import sqlite3
from telebot import types

bot = telebot.TeleBot("6631852490:AAFVkvlGE5iy7qLpaHdNJPW--XkOALUKxVI")
db = sqlite3.connect('register.db')
register = db.cursor()
register.execute('CREATE TABLE IF NOT EXISTS users (user_name TEXT, user_number TEXT, user_id INTEGER);')
supported_languages = 'English', 'Русский'

@bot.message_handler(commands=['start'])
def choose_language(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    global buttons_lang
    buttons_lang = [types.KeyboardButton(lang) for lang in supported_languages]
    keyboard.add(*buttons_lang)

    bot.send_message(message.from_user.id, "Choose your language/Выберите язык:", reply_markup=keyboard)
    bot.register_next_step_handler(message, get_language)

def get_language(message):
    language = message.text
    if language == 'Русский':
        bot.send_message(message.from_user.id, 'Введите свое имя: ', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_name, language)
    elif language == 'English':
        bot.send_message(message.from_user.id, 'Enter your name: ', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_name, language)

def get_name(message, language):
    user_name = message.text
    if language == 'Русский':
        bot.send_message(message.from_user.id, 'Отправьте номер телефона: ', reply_markup=buttons.number_buttons())
        bot.register_next_step_handler(message, get_number, user_name, language)
    elif language == 'English':
        bot.send_message(message.from_user.id, 'Send your number: ', reply_markup=buttons.number_buttons())
        bot.register_next_step_handler(message, get_number, user_name, language)

def get_number(message, user_name, language):
    if language == 'Русский' and message.contact and message.contact.phone_number:
        user_number = message.contact.phone_number
        bot.send_message(message.from_user.id, 'Отлично, теперь отправьте локацию: ', reply_markup=buttons.geo_buttons())
        bot.register_next_step_handler(message, get_location, user_name, user_number, language)
    elif language == 'English' and message.contact and message.contact.phone_number:
        user_number = message.contact.phone_number
        bot.send_message(message.from_user.id, 'Great, now send the location: ', reply_markup=buttons.geo_buttons())
        bot.register_next_step_handler(message, get_location, user_name, user_number, language)
    else:
        if language == 'Русский':
            bot.send_message(message.from_user.id, 'Отправьте номер телефона через кнопку')
            bot.register_next_step_handler(message, get_number, user_name, language)
        elif language == 'English':
            bot.send_message(message.from_user.id, 'Send your phone number via the button')
            bot.register_next_step_handler(message, get_number, user_name, language)

def get_location(message, user_name, user_number, language):
    if message.location:
        user_idd = message.from_user.id
        user_location = message.location
        print(user_name, user_location, user_number, user_idd)
        db = sqlite3.connect('register.db')
        register = db.cursor()
        register.execute('INSERT INTO users (user_name, user_number, user_id) '
                          'VALUES (?, ?, ?);', (user_name, user_number, user_idd))
        db.commit()
        if language == 'Русский':
            bot.send_message(message.from_user.id, 'Спасибо, ваши данные успешно собраны', reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, user_name, user_number, user_location)
        elif language == 'English':
            bot.send_message(message.from_user.id, 'Thank you, your data has been successfully collected', reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, user_name, user_number, user_location)
    else:
        if language == 'Русский':
            bot.send_message(message.from_user.id, 'Отправьте локацию с помощью кнопки')
            bot.register_next_step_handler(message, get_location, user_name, user_number, language)
        if language == 'English':
            bot.send_message(message.from_user.id, 'Submit your location using the button')
            bot.register_next_step_handler(message, get_location, user_name, user_number, language)


bot.infinity_polling()