import unittest

from src.resp.deserializer import decode_to_simple_string


class RESPDeserializerTest(unittest.TestCase):
    def test_decode_to_simple_string(self):
        resp_data = "+Hello, World!\r\n"
        expected = "Hello, World!"
        actual = decode_to_simple_string(resp_data)
        self.assertEqual(expected, actual)

    def test_decode_empty_to_simple_string(self):
        resp_data = "+\r\n"
        expected = ""
        actual = decode_to_simple_string(resp_data)
        self.assertEqual(expected, actual)

    def test_decode_to_bulk_string(self):
        resp_data = "$3\r\nbye\r\n"
        expected = "bye"
        actual = decode_to_bulk_string(resp_data)
        self.assertEquals(expected, actual)

    def test_decode_to_int(self):
        resp_data = ":5\r\n"
        expected = 5
        actual = decode_to_int(resp_data)
        self.assertEquals(expected, actual)

    def test_decode_to_none_array(self):
        resp_data = "*-1\r\n"
        expected = None
        actual = decode_to_array(resp_data)
        self.assertEquals(expected, actual)

    def test_decode_to_none_bulk_string(self):
        resp_data = "$-1\r\n"
        expected = None
        actual = decode_to_bulk_string(resp_data)
        self.assertEquals(expected, actual)

    def test_decode_to_error(self):
        resp_data = "-An error occurred\r\n"
        expected = "An error occurred"
        actual = decode_to_error(resp_data)
        self.assertEquals(expected, actual)

    def test_decode_to_array(self):
        resp_data = "*4\r\n$5\r\nHello\r\n:42\r\n$-1\r\n$5\r\nWorld\r\n"
        expected = ["Hello", 42, None, "World"]
        actual = decode_to_array(resp_data)
        self.assertEquals(expected, actual)

    def test_decode_resp_to_message(self):
        resp_data = "*4\r\n$5\r\nHello\r\n:42\r\n$-1\r\n$5\r\nWorld\r\n"
        expected = ["Hello", 42, None, "World"]
        actual = decode_resp_to_message(resp_data)
        self.assertEquals(expected, actual)
