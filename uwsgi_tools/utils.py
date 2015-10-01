import sys


def sz(x):
    s = hex(x if isinstance(x, int) else len(x))[2:].rjust(4, '0')
    s = bytes.fromhex(s) if sys.version_info[0] == 3 else s.decode('hex')
    return s[::-1]


def pack_uwsgi_vars(var):
    pk = b''
    for k, v in var.items() if hasattr(var, 'items') else var:
        pk += sz(k) + k.encode('utf8') + sz(v) + v.encode('utf8')
    return b'\x00' + sz(pk) + b'\x00' + pk


def parse_addr(addr, default_port=None):
    port = default_port
    if isinstance(addr, str):
        if addr.isdigit():
            addr, port = '', addr
        elif ':' in addr:
            addr, _, port = addr.partition(':')
    elif isinstance(addr, (list, tuple, set)):
        addr, port = addr
    port = int(port) if port else port
    return (addr or '127.0.0.1', port)


def get_host_from_url(url):
    if '//' in url:
        url = url.split('//', 1)[1]
    host, _, url = url.partition('/')
    return (host, url)
