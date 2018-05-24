"""
From definitions available at
http://uwsgi-docs.readthedocs.io/en/latest/Protocol.html
"""

import ctypes


class UwsgiPacketHeader(ctypes.Structure):
    """
    struct uwsgi_packet_header {
        uint8_t modifier1;
        uint16_t datasize;
        uint8_t modifier2;
    }
    """
    _pack_ = 1
    _fields_ = [
        ("modifier1", ctypes.c_int8),
        ("datasize", ctypes.c_int16),
        ("modifier2", ctypes.c_int8),
    ]


class UwsgiVar(object):
    """
    struct uwsgi_var {
        uint16_t key_size;
        uint8_t key[key_size];
        uint16_t val_size;
        uint8_t val[val_size];
    }
    """

    def __new__(self, key_size, key, val_size, val):
        class UwsgiVar(ctypes.Structure):
            _pack_ = 1
            _fields_ = [
                ("key_size", ctypes.c_int16),
                ("key", ctypes.c_char * key_size),
                ("val_size", ctypes.c_int16),
                ("val", ctypes.c_char * val_size),
            ]

        return UwsgiVar(key_size, key, val_size, val)

    @classmethod
    def from_buffer(cls, buffer, offset=0):
        key_size = ctypes.c_int16.from_buffer(buffer, offset).value
        offset += ctypes.sizeof(ctypes.c_int16)
        key = (ctypes.c_char * key_size).from_buffer(buffer, offset).value
        offset += ctypes.sizeof(ctypes.c_char * key_size)
        val_size = ctypes.c_int16.from_buffer(buffer, offset).value
        offset += ctypes.sizeof(ctypes.c_int16)
        val = (ctypes.c_char * val_size).from_buffer(buffer, offset).value

        return cls(key_size, key, val_size, val)
