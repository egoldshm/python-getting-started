#!/usr/bin/python3.6
import csv
import time

from telegram import ReplyKeyboardMarkup, bot

from tools import get_menu_by_father, get_message_by_command


def replace_in_message(message, update):
    first_name = update["from"]["first_name"]
    last_name = update["from"]["last_name"]
    message = message.replace("*|FNAME|*", first_name)
    return message


def get_message_type(message):
    if message[0:5] == "file ":
        return "FILE", message[5:].split(" ")[0], " ".join(message[6:].split(" ")[1:])
    return "TEXT", message, ""


# @app.route('/{}'.format(secret), methods=["POST"])
def on_chat_message(update):
    global save_menu
    print(update)
    if "chat" in update:
        chat = update["chat"]
        chat_id = chat["id"]
        if "text" in update:
            text = update["text"]
            user = update["from"]
            keyboard = get_menu_by_father(text)
            message = get_message_by_command(text)
            message = replace_in_message(message, update)
            if keyboard:
                keyboard = ReplyKeyboardMarkup(keyboard=keyboard)
                save_menu[user["id"]] = text
                bot.sendMessage(chat_id, message, reply_markup=keyboard, parse_mode='Markdown')
            else:
                type_of_message, data, data2 = get_message_type(message)
                if type_of_message == "FILE":
                    print(data)
                    print(data2)
                    bot.sendDocument(chat_id, data, data2)
                else:
                    bot.sendMessage(chat_id, message, parse_mode='Markdown')

        else:
            pass
    else:
        pass
    return "OK"


save_menu = {}
bot.deleteWebhook()
print('Listening ...')
while 1:
    time.sleep(10)
