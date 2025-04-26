def is_simple_string(message: str) -> bool:
    """Function to check if message is a simple string. Simple string must not contain CR(\r) or LF(\n) characters"""
    return (
            isinstance(message, str) and
            (("\r" not in message and "\n" not in message)
            or
            (message.lower() == "ok" or message.lower() == "pong"))
    )


def encode_simple_string(message: str) -> bytes:
    if not is_simple_string(message):
        raise ValueError("Not a valid simple string")
    return f"+{message}\r\n".encode("utf-8")


def encode_int(message: int) -> bytes:
    if not isinstance(message, int):
        raise ValueError("Not a valid integer")
    return f":{message}\r\n".encode("utf-8")


def encode_bulk_string(message: str | None) -> bytes:
    if message is None:
        return b"$-1\r\n"
    return f"${len(message)}\r\n{message}\r\n".encode("utf-8")


def encode_error(message: str) -> bytes:
    return f"-{message}\r\n".encode("utf-8")


def encode_array(message: list[int | str | None]) -> bytes:
    if message == [None]:
        return b"*-1\r\n"
    encoded_items = [encode_message(item).decode("utf-8") for item in message]
    return ("*" + str(len(encoded_items)) + "\r\n" + "".join(encoded_items)).encode("utf-8")


def encode_message(message: str | int | None) -> bytes | None:
    if message is None:
        return encode_bulk_string(message)
    if isinstance(message, list):
        return encode_array(message)
    if is_simple_string(message):
        return encode_simple_string(message)
    if isinstance(message, str):
        return encode_bulk_string(message)
    if isinstance(message, int):
        return encode_int(int(message))
    else:
        raise ValueError("Not a valid message")

def encode_message_to_resp(message: str | int | None | list[int | str | None]) -> bytes:
    return encode_message(message)
