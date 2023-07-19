import re

from src.resp import RESP_TRAILER, EncodingHeader


def decode_to_simple_string(resp_data: str) -> str:
    encoded_pattern = rf"^\{EncodingHeader.SIMPLE_STRING}(.*){RESP_TRAILER}"
    match = re.search(encoded_pattern, resp_data)
    return match.group(1)


def decode_to_bulk_string(resp_data: str) -> str | None:
    encoded_pattern = rf"^\{EncodingHeader.BULK_STRING}([0-9]+){RESP_TRAILER}(.*){RESP_TRAILER}"
    match = re.search(encoded_pattern, resp_data)
    return match.group(2)
