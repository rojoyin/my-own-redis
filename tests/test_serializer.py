import unittest

from src.resp.serializer import encode_simple_string, is_simple_string


class RESPTest(unittest.TestCase):
    def test_serialize_string(self):
        message = "Hello, World!"
        actual = encode_simple_string(message)
        expected = "+Hello, World!\r\n"
        self.assertEquals(actual, expected)

    def test_is_simple_string(self):
        message = "Hello, World!"
        self.assertTrue(is_simple_string(message))

    def test_no_simple_string(self):
        message = "This string contains an LF (\n) character."
        self.assertFalse(is_simple_string(message))

    def test_serialize_int(self):
        message = 5
        actual = encode_int(message)
        expected = ":5\r\n"
        self.assertEquals(actual, expected)

    def test_serialize_array(self):
        message = ["Hello", 42, None, "World"]
        actual = encode_array(message)
        expected = "*4\r\n$5\r\nHello\r\n:42\r\n$-1\r\n$5\r\nWorld\r\n"
        self.assertEquals(actual, expected)

    def test_serialize_bulk_strings(self):
        message = "bye"
        actual = encode_bulk_string(message)
        expected = "$3\r\nbye\r\n"
        self.assertEquals(actual, expected)

    def test_serialize_errors(self):
        message = "An error occurred"
        actual = encode_error(message)
        expected = "-An error occurred\r\n"
        self.assertEquals(actual, expected)

    def test_serialize_empty_bulk_string(self):
        message = ""
        actual = encode_bulk_string(message)
        expected = "$0\r\n\r\n"
        self.assertEquals(actual, expected)

    def test_serialize_null_bulk_string_values(self):
        message = None
        actual = encode_bulk_string(message)
        expected = "$-1\r\n"
        self.assertEquals(actual, expected)

    def test_serialize_null_array_values(self):
        message = None
        actual = encode_array(message)
        expected = "*-1\r\n"
        self.assertEquals(actual, expected)
