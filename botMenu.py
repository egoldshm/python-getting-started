from typing import List, Dict, Optional

COMMAND_NOT_FOUND_MESSAGE = "אוף. הבוט לא הבין מה אתה מחפש 🙁 הוא בסך הכל אוסף של אלגוריתמים - אז הטעות כנראה היא שלך " \
                            "😜 תנסה לחפש במילים אחרות או להשתמש בתפריט... 😉 "
RETURN_MENU_MESSAGE = "חזור 🔁"
RETURN_MESSAGE = "חזרתי 💪"

types = ["photo", "document"]


class BotMenu:

    def __init__(self, commands: List[Dict]):
        print(commands)
        self.commands = commands

    def get_message_type(self, message):
        commands = list(filter(lambda i: i["name"] == message, self.commands))
        if not commands:
            return "text"
        type_of_response = commands[0]["type"]
        return type_of_response

    def response_to_command(self, text):
        result = []
        for i in self.commands:
            if i["is_contact"] == 'FALSE':
                if i["name"] == text:
                    return i["answer"]
            else:
                spaceIndex = i["name"].find(' ')
                firstName = i["name"][:spaceIndex]
                lastName = i["name"][spaceIndex + 1:]
                if firstName in text or lastName in text:
                    if i["name"] in text:
                        return i["answer"]
                    else:
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

    def menu_by_father(self, father_name):

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

        return buttons
