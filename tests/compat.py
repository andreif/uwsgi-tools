import sys

__all__ = ['mock']

PY3 = sys.version_info[0] == 3

if PY3:
    from unittest import mock
else:
    import mock


def str2bytes(s):
    if PY3:
        return bytes(s, encoding='utf8')
    else:
        return s
