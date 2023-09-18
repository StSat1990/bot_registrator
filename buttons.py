from telebot import types

def choose_buttons():
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)

    start_button = types.KeyboardButton('Начать')
    buttons.add(start_button)

    return buttons
def number_buttons():
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)

    contact_button = types.KeyboardButton('Поделиться контактом', request_contact=True)
    buttons.add(contact_button)

    return buttons

def geo_buttons():
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)

    geo_button = types.KeyboardButton('Отправить геолокацию', request_location=True)
    buttons.add(geo_button)

    return buttons