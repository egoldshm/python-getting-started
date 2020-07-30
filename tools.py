from telebot import types

from access_to_google_sheets import *



def get(dict1: dict, string: str) -> str:
    if string in dict1:
        return str(dict1[string])
    return ""


commands = []


def get_dict(_dict: dict) -> str:
    """

    :type _dict: dict
    """
    result = ""
    for i in list(_dict.items()):
        if isinstance(i[1], dict):
            result += "\n" + str(i[0]) + "--\n" + get_dict(i[1]) + "\n"
        elif isinstance(i[1], list):
            result += "\n" + i[0] + "--\n"
            for j in range(0, len(i[1])):
                if isinstance(i[1][j], dict):
                    result += str(j) + ": " + get_dict(i[1][j]) + "\n"
        else:
            result += "\n" + str(i[0]) + ": " + str(i[1])

    return result[1:]


def get_message_by_command(text):
    for i in commands:
        if i["name"] == text:
            return i["answer"]
    return "לא נמצא!"


def get_menu_by_father(father_name):
    global commands
    commands_for_menu = list(filter(lambda i: i["father_menu"] == father_name, commands))
    left_buttons = []
    rows_list = list(map(lambda i: int(i["row"]) if i["row"].isdigit() else 0, commands_for_menu))
    if rows_list == []:
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

    # return buttons

    # make to keyboard format
    markup = types.ReplyKeyboardMarkup()

    for row in buttons:
        list_of_buttons = []
        for item in row:
            list_of_buttons.append(types.KeyboardButton(item))
        markup.add(*list_of_buttons)
    return markup


def reset_bot():
    global commands
    commands = get_data_from_file()
    print(get_menu_by_father("/start"))

reset_bot()