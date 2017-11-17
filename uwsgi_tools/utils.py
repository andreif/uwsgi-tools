from .compat import hex2bytes, urlsplit


def sz(x):
    s = hex(x if isinstance(x, int) else len(x))[2:].rjust(4, '0')
    s = hex2bytes(s)
    return s[::-1]


def pack_uwsgi_vars(var):
    pk = b''
    for k, v in var.items() if hasattr(var, 'items') else var:
        pk += sz(k) + k.encode('utf8') + sz(v) + v.encode('utf8')
    return b'\x00' + sz(pk) + b'\x00' + pk


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
