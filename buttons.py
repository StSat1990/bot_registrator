from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery

def language_buttons():
    buttons = InlineKeyboardMarkup(row_width=2)

    language_ru = InlineKeyboardButton(text='Русский', callback_data='ru')
    language_eng = InlineKeyboardButton(text='Английский', callback_data='eng')

    buttons.row(language_ru, language_eng)

    return buttons

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