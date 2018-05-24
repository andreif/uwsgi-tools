from .compat import struct2bytes, urlsplit
from .uwsgi_structs import UwsgiPacketHeader, UwsgiVar


def pack_uwsgi_vars(var):
    encoded_vars = [
        (k.encode('utf-8'), v.encode('utf-8'))
        for k, v in var.items()
    ]
    packed_vars = b''.join(
        struct2bytes(UwsgiVar(len(k), k, len(v), v))
        for k, v in encoded_vars
    )
    packet_header = struct2bytes(UwsgiPacketHeader(0, len(packed_vars), 0))
    return packet_header + packed_vars


def parse_addr(addr, default_port=3030):
    host = None
    port = None
    if isinstance(addr, str):
        if addr.isdigit():
            port = addr
        else:
            parts = urlsplit('//' + addr)
            host = parts.hostname
            port = parts.port
    elif isinstance(addr, (list, tuple, set)):
        host, port = addr
    return (host or '127.0.0.1',
            int(port) if port else default_port)


def get_host_from_url(url):
    # TODO: error for https
    url = url.split('://')[-1]

    if url and url[0] != '/':
        # TODO: validate hostname
        host, _, url = url.partition('/')
        return (host, '/' + url)

    return '', url
