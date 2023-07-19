import re


def decode_to_simple_string(resp_data: str) -> str:
    encoded_pattern = r"^\+(.*)\r\n"
    match = re.search(encoded_pattern, resp_data)
    return match.group(1)
