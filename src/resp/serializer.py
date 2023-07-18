def is_simple_string(message):
    """Function to check if message is a simple string. Simple string must not contain CR(\r) or LF(\n) characters"""
    return "\r" not in message and "\n" not in message


def encode_simple_string(message):
    if not is_simple_string(message):
        raise ValueError("Not a valid simple string")
    return f"+{message}\r\n"


def encode_int(message):
    if not isinstance(message, int):
        raise ValueError("Not a valid integer")
    return f":{message}\r\n"


def encode_bulk_string(message):
    return f"${len(message)}\r\n{message}\r\n"


def encode_error(message):
    return f"-{message}\r\n"
