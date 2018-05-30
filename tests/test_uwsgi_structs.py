import unittest

from uwsgi_tools import uwsgi_structs as uw


class TestUwsgiPacketHeader(unittest.TestCase):
    header = uw.UwsgiPacketHeader(0, 166, 0)
    header_bytes = b'\x00\xa6\x00\x00'

    def test_packet_header_serializes(self):
        expected = self.header_bytes

        self.assertEqual(expected, bytearray(self.header))

    def test_packet_header_deserializes(self):
        buffer = bytearray(self.header_bytes)
        expected_header = uw.UwsgiPacketHeader(0, 166, 0)

        header = uw.UwsgiPacketHeader.from_buffer(buffer)
        self.assertEqual(
            bytearray(expected_header),
            bytearray(header)
        )


class TestUwsgiVar(unittest.TestCase):
    key = b'foo'
    key_size = len(key)
    val = b'bar'
    val_size = len(val)
    var = uw.UwsgiVar(key_size, key, val_size, val)
    var_bytes = b'\x03\x00foo\x03\x00bar'

    def test_var_serializes(self):
        self.assertEqual(
            self.var_bytes,
            bytearray(self.var)
        )

    def test_var_deserializes(self):
        buffer = bytearray(self.var_bytes)
        expected = self.var

        var = uw.UwsgiVar.from_buffer(buffer)
        self.assertEqual(
            bytearray(expected),
            bytearray(var)
        )
