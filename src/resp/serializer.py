def is_simple_string(message: str) -> bool:
    """Function to check if message is a simple string. Simple string must not contain CR(\r) or LF(\n) characters"""
    return "\r" not in message and "\n" not in message


def encode_simple_string(message: str) -> str:
    if not is_simple_string(message):
        raise ValueError("Not a valid simple string")
    return f"+{message}\r\n"


def encode_int(message: int) -> str:
    if not isinstance(message, int):
        raise ValueError("Not a valid integer")
    return f":{message}\r\n"


def encode_bulk_string(message: str | None) -> str:
    if message is None:
        return "$-1\r\n"
    return f"${len(message)}\r\n{message}\r\n"


def encode_error(message: str) -> str:
    return f"-{message}\r\n"


def encode_array(message: list[int | str | None]) -> str:
    if message is None:
        return "*-1\r\n"
    encoded_items = [encode_message(item) for item in message]
    return "*" + str(len(encoded_items)) + "\r\n" + "".join(encoded_items)


def encode_message(message: str | int | None) -> str:
    if message is None:
        return encode_bulk_string(message)
    if isinstance(message, str):
        return encode_bulk_string(message)
    if isinstance(message, int):
        return encode_int(int(message))


def encode_message_to_resp(message: str | int | None | list[int | str | None]) -> str:
    if isinstance(message, list):
        return encode_array(message)

    return encode_message(message)
