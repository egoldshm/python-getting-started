import User
from values_to_bot import data_to_bot
from botMenu import get_message_type, RETURN_MENU_MESSAGE, RETURN_MESSAGE

RESET_MESSAGE = "reset commands 123"


class Telegram_menu_bot:
    def __init__(self):
        self.data_to_bot = data_to_bot()
        self.botMenu = self.data_to_bot.botMenu
        self.save_menu = {}
        print("check")

    def messageHandler(self, chat_id, bot, user: User, text):
        try:
            print(str(user) + "\t" + str(text))

            keyboard = self.botMenu.menu_by_father(text)

            message = self.botMenu.response_to_command(text)

            message = user.replace_in_message(message)

            if text == RETURN_MENU_MESSAGE:
                keyboard = self.botMenu.menu_by_father("/start")
                message = RETURN_MESSAGE

            if text == RESET_MESSAGE:
                self.data_to_bot.reset()
                self.botMenu = self.data_to_bot.botMenu

            if keyboard:
                # if we got new keyboard
                self.save_menu[user.id] = text
                bot.IsendMessage(chat_id, message, keyboard)

            else:
                type_of_message, data, data2 = get_message_type(message)
                if type_of_message == "FILE":
                    bot.IsendMessage(chat_id, data, data2)
                else:
                    bot.IsendMessage(chat_id, message, None)
            return "Done"
        except Exception as ex:
            print("ERROR: " + str(ex))
            return "ERROR"


