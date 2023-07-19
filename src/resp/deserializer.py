import re

from src.resp import RESP_TRAILER, EncodingHeader


def decode_to_simple_string(resp_data: str) -> str:
    encoded_pattern = rf"^\{EncodingHeader.SIMPLE_STRING}(.*){RESP_TRAILER}"
    match = re.search(encoded_pattern, resp_data)
    return match.group(1)
