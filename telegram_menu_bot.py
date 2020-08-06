import telebot
from telebot import types

from MessageHandler import Telegram_menu_bot
from User import User

TOKEN: str = "833051014:AAENxwuWjOM_TZcqPE-c5niOUuTq66MaC2g"
bot = telebot.TeleBot(TOKEN)


def list_of_lists_to_keyboards(buttons):
    markup = types.ReplyKeyboardMarkup()
    for row in buttons:
        list_of_buttons = []
        for item in row:
            list_of_buttons.append(types.KeyboardButton(item))
        markup.add(*list_of_buttons)
    return markup


class TelepbotBot:
    def __init__(self, bot_p):
        self.bot = bot_p

    def IsendMessage(self, chat_id, message, keyboard=None, mark_down=True):
        keyboard = self.get_valid_keyboard(keyboard)
        self.bot.send_message(chat_id, message, parse_mode='Markdown' if mark_down else None, reply_markup=keyboard)

    def IsendFile(self, chat_id, file_id, text=None, keyboard=None):
        keyboard = self.get_valid_keyboard(keyboard)
        self.bot.send_document(chat_id, file_id, caption=text, reply_markup=keyboard, parse_mode='Markdown')

    def IsendPhoto(self, chat_id, photo_id, text, keyboard=None):
        keyboard = self.get_valid_keyboard(keyboard)
        self.bot.send_photo(chat_id, photo_id, caption=text, reply_markup=keyboard, parse_mode='Markdown')

    def get_valid_keyboard(self, keyboard):
        if keyboard and not isinstance(keyboard, str):
            keyboard = list_of_lists_to_keyboards(keyboard)
        else:
            keyboard = None
        return keyboard


@bot.message_handler(func=lambda message: True,
                     content_types=['audio', 'photo', 'voice', 'video', 'document', 'text', 'location', 'contact',
                                    'sticker'])
def answer(update):
    telepbotBot = TelepbotBot(bot)
    chat = update.chat
    chat_id = chat.id
    text = update.text

    user = update.from_user
    print(user)
    user_p = User(user.id, user.first_name, user.last_name, user.username)

    telegram_menu_bot = Telegram_menu_bot()

    return telegram_menu_bot.messageHandler(chat_id, telepbotBot, user_p, text)


bot.polling()
