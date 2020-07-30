def get(dict1: dict, string: str) -> str:
    if string in dict1:
        return str(dict1[string])
    return ""


commands = []


def get_dict(_dict: dict) -> str:
    """
    helper function - get dict in format printable

    :type _dict: dict
    """
    result = ""
    for key, value in _dict.items():
        if isinstance(value, dict):
            result += "\n" + str(key) + "--\n" + get_dict(value) + "\n"
        elif isinstance(value, list):
            result += "\n" + key + "--\n"
            for j in range(0, len(value)):
                if isinstance(value[j], dict):
                    result += str(j) + ": " + get_dict(value[j]) + "\n"
        else:
            result += "\n" + str(key) + ": " + str(value)

    return result[1:]