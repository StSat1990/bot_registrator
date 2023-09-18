import telebot
import buttons
import sqlite3

bot = telebot.TeleBot("6445153794:AAGn-vttxJSCdl21iQcLlLa5SHpTZL3Mm90")
db = sqlite3.connect('register.db')
register = db.cursor()
register.execute('CREATE TABLE IF NOT EXISTS users (user_name TEXT, user_number TEXT, user_id INTEGER);')
@bot.message_handler(commands=['start'])
def start_mybot(message):
    global user_id
    user_id = message.from_user.id
    bot.send_message(user_id, message.from_user.username + ', добро пожаловать!', reply_markup=buttons.choose_buttons())

@bot.message_handler(content_types=['text'])
def start_bot_text(message):
    if message.text == 'Начать':
        bot.send_message(user_id, 'Напишите свое имя: ', reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_name)
def get_name(message):
    user_name = message.text
    bot.send_message(user_id, 'Отправьте номер телефона: ', reply_markup=buttons.number_buttons())
    bot.register_next_step_handler(message, get_number, user_name)

def get_number(message, user_name):
    if message.contact and message.contact.phone_number:
        user_number = message.contact.phone_number
        bot.send_message(user_id, 'Отлично, теперь отправьте локацию: ', reply_markup=buttons.geo_buttons())
        bot.register_next_step_handler(message, get_location, user_name, user_number)
    else:
        bot.send_message(user_id, 'Отправьте номер телефона через кнопку')
        bot.register_next_step_handler(message, user_name, get_number)
def get_location(message, user_name, user_number):
    if message.location:
        user_idd = message.from_user.id
        user_location = message.location
        print(user_name, user_location, user_number, user_idd)
        db = sqlite3.connect('register.db')
        register = db.cursor()
        register.execute('INSERT INTO users (user_name, user_number, user_id) '
                          'VALUES (?, ?, ?);', (user_name, user_number, user_idd))
        db.commit()
        bot.send_message(user_id, 'Спасибо, ваши данные успешно собраны ', reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, start_bot_text, user_name, user_number, user_location)
    else:
        bot.send_message(user_id, 'Отправьте локацию с помощью кнопки')
        bot.register_next_step_handler(message, get_location, user_name, user_number)


bot.infinity_polling()