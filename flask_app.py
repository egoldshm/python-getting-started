#!/usr/bin/python3.6
import csv
import time

from flask import Flask, request
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from tools import *

# proxy_url = "http://proxy.server:3128"
# telepot.api._pools = {
#    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
# }
# telepot.api._onetime_pool_spec = (
#    urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

# secret = "7cca0cb2-17fc-4519-b0f4-f6d7dfdc2941"
bot = telepot.Bot("1085962867:AAHQyGzmCyKJDfXGNmBgGVpt6Knb_eSzdE8")


def replace_in_message(message, update):
    first_name = update["from"]["first_name"]
    last_name = update["from"]["last_name"]
    message = message.replace("*|FNAME|*", first_name)
    return message


def get_message_type(message):
    if message[0:5] == "file ":
        return "FILE", message[5:].split(" ")[0], " ".join(message[6:].split(" ")[1:])
    return "TEXT", message, ""


# bot.setWebhook("https://egoldshm.pythonanywhere.com/{}".format(secret), max_connections=1)

# app = Flask(__name__)


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
MessageLoop(bot, {'chat': on_chat_message}).run_forever()
print('Listening ...')
while 1:
    time.sleep(10)
