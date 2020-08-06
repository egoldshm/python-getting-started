class User:
    id: int
    f_name: str
    l_name: str
    username: str

    def __init__(self, user_id: int, first_name: str, last_name: str, username: str) -> None:
        self.id = user_id
        self.f_name = str(first_name)
        self.l_name = str(last_name)
        self.username = str(username)

    def replace_in_message(self, text):
        text = text.replace("*|FNAME|*", self.f_name if self.f_name else "")
        text = text.replace("*|LNAME|*", self.l_name if self.l_name else "")
        return text

    def __str__(self):
        return """מספר זיהוי: {}
        שם פרטי: {}
        שם משפחה: {}
        שם משתמש: {}""".format(self.id, self.f_name, self.l_name, self.username)