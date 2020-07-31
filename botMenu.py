from typing import List, Dict, Optional

from telebot import types
from telebot.types import ReplyKeyboardMarkup

COMMAND_NOT_FOUND_MESSAGE = "לא נמצא!"
RETURN_MENU_MESSAGE = "חזור 🔁"
RETURN_MESSAGE = "חזרתי 💪"


def list_of_lists_to_keyboards(buttons: List[List[str]]) -> ReplyKeyboardMarkup:
    # make to keyboard format
    markup = types.ReplyKeyboardMarkup()
    for row in buttons:
        list_of_buttons = []
        for item in row:
            list_of_buttons.append(types.KeyboardButton(item))
        markup.add(*list_of_buttons)
    return markup


def get_message_type(message):
    if message[0:5] == "file ":
        return "FILE", message[5:].split(" ")[0], " ".join(message[6:].split(" ")[1:])
    return "TEXT", message, ""


def replace_in_message(message, first_name, last_name):
    message = message.replace("*|FNAME|*", first_name if first_name else "")
    message = message.replace("*|LNAME|*", last_name if last_name else "")
    return message


class BotMenu:

    def __init__(self, commands: List[Dict]):
        print(commands)
        self.commands = commands

    def response_to_command(self, text):
        result = []
        for i in self.commands:
            if i["name"] == text and i["substring"] == 'FALSE':
                return i["answer"]
            if i["name"] in text and i["substring"] == 'TRUE':
                if i["answer"] not in result:
                    result.append(i["answer"])
        if result:
            return "\n".join(result)
        return COMMAND_NOT_FOUND_MESSAGE

    def menu_return(self, menu_name) -> Optional[str]:
        fathers = list(filter(lambda i: i["name"] == menu_name, self.commands))
        if len(fathers) == 0:
            return None
        father_menu = fathers[0]["father_menu"]
        return father_menu

    def menu_by_father(self, father_name) -> Optional[ReplyKeyboardMarkup]:

        # take only command that father_menu is father name
        commands_for_menu = list(filter(lambda i: i["father_menu"] == father_name, self.commands))

        left_buttons = []

        # get the rows of the commands
        rows_list = list(map(lambda i: int(i["row"]) if i["row"].isdigit() else 0, commands_for_menu))

        if not rows_list:
            return None

        max_row = max(rows_list)
        buttons = []
        for i in range(max_row + 1):
            columns = [int(j["column"]) for j in commands_for_menu if j["row"] == str(i)]
            max_column = max([1] if columns == [] else (columns))
            buttons.append(["" for j in range(max_column + 1)])
        for i in commands_for_menu:
            if not i["row"].isdigit() or not i["column"].isdigit():
                left_buttons.append(i["name"])
            else:
                buttons[int(i["row"])][int(i["column"])] = i["name"]
        for i in left_buttons:
            buttons.append([i])

        if self.menu_return(father_name) != "":
            buttons.append([RETURN_MENU_MESSAGE])

        return list_of_lists_to_keyboards(buttons)
