from enum import StrEnum

RESP_TRAILER = "\r\n"


class EncodingHeader(StrEnum):
    SIMPLE_STRING = "+"
    ERROR = "-"
    INTEGER = ":"
    BULK_STRING = "$"
    ARRAY = "*"
