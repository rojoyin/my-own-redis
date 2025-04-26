import unittest

from my_own_redis.resp.serializer import encode_simple_string, is_simple_string, encode_int, encode_bulk_string, encode_error, \
    encode_array, encode_message_to_resp


class RESPTest(unittest.TestCase):
    def test_serialize_string(self):
        message = "Hello, World!"
        actual = encode_simple_string(message)
        expected = b"+Hello, World!\r\n"
        self.assertEqual(actual, expected)

    def test_is_simple_string(self):
        message = "Hello, World!"
        self.assertTrue(is_simple_string(message))

    def test_no_simple_string(self):
        message = "This string contains an LF (\n) character."
        self.assertFalse(is_simple_string(message))

    def test_error_raise_no_simple_string(self):
        message = "Invalid\rSimple String"
        with self.assertRaises(ValueError):
            encode_simple_string(message)

    def test_serialize_int(self):
        message = 5
        actual = encode_int(message)
        expected = b":5\r\n"
        self.assertEqual(actual, expected)

    def test_error_no_int(self):
        message = 2.8
        with self.assertRaises(ValueError):
            encode_int(message)

    def test_serialize_bulk_strings(self):
        message = "bye"
        actual = encode_bulk_string(message)
        expected = b"$3\r\nbye\r\n"
        self.assertEqual(actual, expected)

    def test_serialize_empty_bulk_string(self):
        message = ""
        actual = encode_bulk_string(message)
        expected = b"$0\r\n\r\n"
        self.assertEqual(actual, expected)

    def test_serialize_errors(self):
        message = "An error occurred"
        actual = encode_error(message)
        expected = b"-An error occurred\r\n"
        self.assertEqual(actual, expected)

    def test_serialize_null_bulk_string_values(self):
        message = None
        actual = encode_bulk_string(message)
        expected = b"$-1\r\n"
        self.assertEqual(actual, expected)

    def test_serialize_null_array_values(self):
        message = [None]
        actual = encode_array(message)
        expected = b"*-1\r\n"
        self.assertEqual(actual, expected)

    def test_serialize_array(self):
        message = ["Hello", 42, None, "World"]
        actual = encode_array(message)
        expected = b"*4\r\n+Hello\r\n:42\r\n$-1\r\n+World\r\n"
        self.assertEqual(actual, expected)

    def test_encode_message_to_resp(self):
        message = "holi"
        actual = encode_message_to_resp(message)
        expected = b"+holi\r\n"
        self.assertEqual(actual, expected)
