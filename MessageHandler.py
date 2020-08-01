import User
from getAdmins import getAdmins
from save_data_in_file import Save_data_in_file
from values_to_bot import data_to_bot
from botMenu import RETURN_MENU_MESSAGE, RETURN_MESSAGE

RESET_MESSAGE = "reset"
FILENAME_registered_users = "registered_users.txt"
SEND_MESSAGE_TO_ALL = "שלח לכולם:\n"


def report_to_channel(bot, message, text, user):
    try:
        bot.IsendMessage(-1001205958777, """משתמש: {}
        הודעה 💬: {}
        תשובה 🗨 : {}""".format(user, text, message))
    except:
        print("Not find channel")


def splitMessage(message):
    split_list = message.split(" ")
    if len(split_list) > 1:
        return split_list[0], " ".join(split_list[1:])
    return message, None


class Telegram_menu_bot:
    def __init__(self):
        self.data_to_bot = data_to_bot()
        self.botMenu = self.data_to_bot.botMenu
        self.save_menu = {}
        self.registered_users = Save_data_in_file(FILENAME_registered_users)
        self.admins = getAdmins()
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

            if user.id in self.admins:
                if text == RESET_MESSAGE:
                    self.data_to_bot.reset()
                    self.botMenu = self.data_to_bot.botMenu
                    message = "התפריט אופס בהצלחה! 👌 "

                elif SEND_MESSAGE_TO_ALL in text:
                    text_to_send = text.replace(SEND_MESSAGE_TO_ALL, "")
                    count = 0
                    for user_id in self.registered_users.data:
                        try:
                            bot.IsendMessage(user_id, text_to_send)
                            count += 1
                        except:
                            pass
                    message = "ההודעה נשלחה בהצלחה ל{} משתמשים".format(count)

            if keyboard:
                # if we got new keyboard
                self.save_menu[user.id] = text
                bot.IsendMessage(chat_id, message, keyboard)

            else:
                type_of_message = self.botMenu.get_message_type(text)
                first, second = splitMessage(message)
                if type_of_message == "photo":
                    bot.IsendPhoto(chat_id, first, second)
                if type_of_message == "file":
                    bot.IsendFile(chat_id, first, second)
                else:
                    bot.IsendMessage(chat_id, first)

            report_to_channel(bot, message, text, user)

            self.registered_users.add_name(str(user.id))

            return "Done"
        except Exception as ex:
            print("ERROR: " + str(ex))
            return "ERROR"
