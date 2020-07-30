import telebot
from telebot import types

from botMenu import replace_in_message, get_message_type, RETURN_MENU_MESSAGE, RETURN_MESSAGE
from values_to_bot import data_to_bot

TOKEN: str = "1085962867:AAHQyGzmCyKJDfXGNmBgGVpt6Knb_eSzdE8"

bot = telebot.TeleBot(TOKEN)


class telegram_menu_bot:
    def __init__(self):
        self.data_to_bot = data_to_bot()
        self.botMenu = self.data_to_bot.botMenu
        self.save_menu = {}
        print("check")


menu_bot = telegram_menu_bot()


@bot.message_handler(func=lambda message: True)
def answer(update):
    chat = update.chat
    chat_id = chat.id
    text = update.text
    user = update.from_user

    keyboard = menu_bot.botMenu.menu_by_father(text)

    message = menu_bot.botMenu.response_to_command(text)

    message = replace_in_message(message, update.from_user.first_name, update.from_user.last_name)

    if text == RETURN_MENU_MESSAGE:
        keyboard = menu_bot.botMenu.menu_return(menu_bot.save_menu[user.id])
        message = RETURN_MESSAGE

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


bot.polling()
