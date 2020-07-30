#!/usr/bin/env python
import os
import sys

import telebot
from telebot import types
from telepot.namedtuple import ReplyKeyboardMarkup

save_menu = {}

from tools import *

def replace_in_message(message, update):
    first_name = update.from_user.first_name
    last_name = update.from_user.last_name
    message = message.replace("*|FNAME|*", first_name)
    return message


def get_message_type(message):
    if message[0:5] == "file ":
        return "FILE", message[5:].split(" ")[0], " ".join(message[6:].split(" ")[1:])
    return "TEXT", message, ""


# @app.route('/{}'.format(secret), methods=["POST"])

TOKEN = "1085962867:AAHQyGzmCyKJDfXGNmBgGVpt6Knb_eSzdE8"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def answer(update):
    global save_menu

    chat = update.chat
    chat_id = chat.id
    text = update.text
    user = update.from_user
    keyboard = get_menu_by_father(text)
    print(keyboard)
    message = get_message_by_command(text)

    message = replace_in_message(message, update)
    if keyboard:
        save_menu[user.id] = text
        bot.send_message(chat_id, message, reply_markup=keyboard, parse_mode='Markdown')
    else:
        type_of_message, data, data2 = get_message_type(message)
        if type_of_message == "FILE":
            print(data)
            print(data2)
            bot.send_document(chat_id, data, data2)
        else:
            markup = types.ReplyKeyboardRemove(selective=False)
            bot.send_message(chat_id, message, reply_markup=markup)
    return "OK"


bot.polling()
