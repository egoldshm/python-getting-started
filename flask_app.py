from typing import List

import telepot
import urllib3
from flask import Flask, request
from telepot.namedtuple import ReplyKeyboardMarkup

from botMenu import replace_in_message, get_message_type, RETURN_MENU_MESSAGE, RETURN_MESSAGE
from values_to_bot import data_to_bot

TOKEN: str = "1391323439:AAEog24qd0XYB3O--OANiGUWOvU0elcPXT0"
RESET_MESSAGE = "reset commands 123"
secret = "7bd8040d-baff-41c2-b16f-cdffb6e168f0"

proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (
    urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

bot = telepot.Bot(TOKEN)
bot.setWebhook("https://yatmal.pythonanywhere.com/{}".format(secret), max_connections=1)

app = Flask(__name__)


class telegram_menu_bot:
    def __init__(self):
        self.data_to_bot = data_to_bot()
        self.botMenu = self.data_to_bot.botMenu
        self.save_menu = {}
        print("check")


menu_bot = telegram_menu_bot()


def list_of_lists_to_keyboards(buttons: List[List[str]]):
    return ReplyKeyboardMarkup(keyboard=buttons)
    #
    # make to keyboard format - telebot: old.
    # markup = types.ReplyKeyboardMarkup()
    # for row in buttons:
    #    list_of_buttons = []
    #    for item in row:
    #        list_of_buttons.append(types.KeyboardButton(item))
    #    markup.add(*list_of_buttons)
    # return markup"""


@app.route('/{}'.format(secret), methods=["POST"])
def answer():
    try:
        update = request.get_json()

        if "message" not in update:
            print("problem with 'message'")
            print(str(update))
        message = update["message"]
        if "text" not in message:
            print("problem with text")
            print(str(message))
        if "chat" not in message:
            print("problem with chat")
            print(str(message))

        chat = message["chat"]
        chat_id = chat["id"]
        text = message["text"]

        user = message["from"]

        print(str(user) + "\t" + str(text))

        keyboard = list_of_lists_to_keyboards(menu_bot.botMenu.menu_by_father(text))

        message = menu_bot.botMenu.response_to_command(text)

        message = replace_in_message(message, user["first_name"], user["last_name"])

        if text == RETURN_MENU_MESSAGE:
            keyboard = list_of_lists_to_keyboards(menu_bot.botMenu.menu_by_father("/start"))
            message = RETURN_MESSAGE

        if text == RESET_MESSAGE:
            menu_bot.data_to_bot.reset()
            menu_bot.botMenu = menu_bot.data_to_bot.botMenu

        if keyboard:
            # if we got new keyboard
            menu_bot.save_menu[user["id"]] = text
            bot.sendMessage(chat_id, message, reply_markup=keyboard)

        else:
            type_of_message, data, data2 = get_message_type(message)
            if type_of_message == "FILE":
                bot.sendMessage(chat_id, data, data2)
            else:
                bot.sendMessage(chat_id, message)
        return "Done"
    except Exception as ex:
        print("ERROR: " + str(ex))
        return "ERROR"
