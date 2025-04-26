import re
from typing import List

from my_own_redis.resp import RESP_TRAILER, EncodingHeader


def decode_to_simple_string(resp_data: str) -> str:
    encoded_pattern = rf"^\{EncodingHeader.SIMPLE_STRING}(.*){RESP_TRAILER}"
    match = re.search(encoded_pattern, resp_data)
    return match.group(1)


def decode_to_bulk_string(resp_data: str) -> str | None:
    if resp_data == "$-1\r\n":
        return None

    encoded_pattern = rf"^\{EncodingHeader.BULK_STRING}([0-9]+){RESP_TRAILER}(.*){RESP_TRAILER}"
    match = re.search(encoded_pattern, resp_data)
    return match.group(2)


def decode_to_int(resp_data: str) -> int:
    encoded_pattern = rf"^\{EncodingHeader.INTEGER}([0-9]+){RESP_TRAILER}"
    match = re.search(encoded_pattern, resp_data)
    return int(match.group(1))


def decode_to_error(resp_data: str) -> str:
    encoded_pattern = rf"^\{EncodingHeader.ERROR}(.*){RESP_TRAILER}"
    match = re.search(encoded_pattern, resp_data)
    return match.group(1)


def decode_to_array(resp_data: str) -> List[int | None | str]:
    if resp_data == "*-1\r\n":
        return [None]

    encoded_pattern = rf"^\{EncodingHeader.ARRAY}(\d+)\r\n([\S\s]*)"
    match = re.search(encoded_pattern, resp_data)
    encoded_messages = match.group(2)
    decoded_messages = []
    i = 0
    while i < len(encoded_messages):
        encoding_symbol = encoded_messages[i]

        if encoding_symbol == EncodingHeader.BULK_STRING:
            modifier = encoded_messages[i+1]
            if modifier == "-":
                decoded_messages.append(None)
                i += len("$-1\r\n")
                continue

            string_size = int(modifier)
            chunk_size = string_size + len(encoded_messages[i + 1]) + 2 * len(RESP_TRAILER) + 1
            string_to_encode = encoded_messages[i:i+chunk_size]
            decoded_messages.append(decode_to_bulk_string(string_to_encode))
            i += chunk_size
            continue

        if encoding_symbol == EncodingHeader.INTEGER:
            chunk_size = 0
            j = i
            while encoded_messages[i] != "\r":
                chunk_size += 1
                i += 1

            chunk_size += len(RESP_TRAILER)
            string_to_encode = encoded_messages[j:j+chunk_size]
            decoded_messages.append(decode_to_int(string_to_encode))
            i = j
            i += chunk_size
            continue

    return decoded_messages


def decode_resp_to_message(resp_data: str) -> str | int | None | List[int | str | None]:
    if resp_data.startswith(EncodingHeader.BULK_STRING):
        return decode_to_bulk_string(resp_data)
    if resp_data.startswith(EncodingHeader.SIMPLE_STRING):
        return decode_to_simple_string(resp_data)
    if resp_data.startswith(EncodingHeader.INTEGER):
        return decode_to_int(resp_data)
    if resp_data.startswith(EncodingHeader.ERROR):
        return decode_to_error(resp_data)
    if resp_data.startswith(EncodingHeader.ARRAY):
        return decode_to_array(resp_data)
