import sys

__all__ = [
    'BaseHTTPRequestHandler', 'TCPServer', 'get_content_type', 'urlsplit',
    'hex2bytes',
]

PY3 = sys.version_info[0] == 3


if PY3:
    from http.server import BaseHTTPRequestHandler
    from socketserver import TCPServer
    from urllib.parse import urlsplit
else:
    from BaseHTTPServer import BaseHTTPRequestHandler
    from SocketServer import TCPServer
    from urlparse import urlsplit


def get_content_type(headers):
    if PY3:
        return headers.get('content-type')
    else:
        return headers.typeheader


def hex2bytes(s):
    if PY3:
        return bytes.fromhex(s)
    else:
        return s.decode('hex')
