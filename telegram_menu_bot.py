import os

from telegram.ext import Updater, MessageHandler

from botMenu import replace_in_message, get_message_type, RETURN_MENU_MESSAGE, RETURN_MESSAGE
from values_to_bot import data_to_bot

PORT = int(os.environ.get('PORT', 5000))

TOKEN: str = "1085962867:AAHQyGzmCyKJDfXGNmBgGVpt6Knb_eSzdE8"
RESET_MESSAGE = "reset commands 123"


class telegram_menu_bot:
    def __init__(self):
        self.data_to_bot = data_to_bot()
        self.botMenu = self.data_to_bot.botMenu
        self.save_menu = {}
        print("check")


menu_bot = telegram_menu_bot()

updater = Updater(TOKEN)

bot = updater.bot


# @bot.message_handler(func=lambda message: True)
def answer(update):
    try:
        chat = update.chat
        chat_id = chat.id
        text = update.text
        user = update.from_user

        print(str(user) + "\t" + text)

        keyboard = menu_bot.botMenu.menu_by_father(text)

        message = menu_bot.botMenu.response_to_command(text)

        message = replace_in_message(message, update.from_user.first_name, update.from_user.last_name)

        if text == RETURN_MENU_MESSAGE:
            keyboard = menu_bot.botMenu.menu_by_father(menu_bot.botMenu.menu_return(menu_bot.save_menu[user.id]))
            message = RETURN_MESSAGE

        if text == RESET_MESSAGE:
            menu_bot.data_to_bot.reset()
            menu_bot.botMenu = menu_bot.data_to_bot.botMenu

        if keyboard:
            # if we got new keyboard
            menu_bot.save_menu[user.id] = text
            bot.send_message(chat_id, message, reply_markup=keyboard, parse_mode='Markdown')
        else:
            type_of_message, data, data2 = get_message_type(message)
            if type_of_message == "FILE":
                bot.send_document(chat_id, data, data2)
            else:
                bot.send_message(chat_id, message)
        return "OK"
    except Exception as ex:
        print("ERROR!\n" + str(ex))
        pass


mode = os.getenv("MODE")


def run(updater):
    PORT = int(os.environ.get("PORT", "8443"))
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
    # Code from https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)

    print(HEROKU_APP_NAME)
    updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
    updater.idle()


updater = Updater(TOKEN, use_context=True)

updater.dispatcher.add_handler(MessageHandler(lambda _: True, answer))

run(updater)
