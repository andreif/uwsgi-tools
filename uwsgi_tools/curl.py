import socket
import sys
from .compat import urlsplit
from .utils import pack_uwsgi_vars, parse_addr, get_host_from_url


def ask_uwsgi(uwsgi_addr, var, body='', timeout=0, udp=False):
    sock_type = socket.SOCK_DGRAM if udp else socket.SOCK_STREAM
    if isinstance(uwsgi_addr, str) and '/' in uwsgi_addr:
        addr = uwsgi_addr
        s = socket.socket(family=socket.AF_UNIX, type=sock_type)
    else:
        addr = parse_addr(addr=uwsgi_addr)
        s = socket.socket(*socket.getaddrinfo(
            addr[0], addr[1], 0, sock_type)[0][:2])

    if timeout:
        s.settimeout(timeout)

    if body is None:
        body = ''

    s.connect(addr)
    s.send(pack_uwsgi_vars(var) + body.encode('utf8'))
    response = []
    while 1:
        data = s.recv(4096)
        if not data:
            break
        response.append(data)
    s.close()
    return b''.join(response).decode('utf8')


def curl(uwsgi_addr, url, method='GET', body='', timeout=0, headers=(),
         udp=False):
    host, uri = get_host_from_url(url)
    parts_uri = urlsplit(uri)

    if '/' not in uwsgi_addr:
        addr = parse_addr(addr=uwsgi_addr)
        if not host:
            host = addr[0]
        port = addr[1]
    else:
        port = None

    var = {
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'PATH_INFO': parts_uri.path,
        'REQUEST_METHOD': method.upper(),
        'REQUEST_URI': uri,
        'QUERY_STRING': parts_uri.query,
        'HTTP_HOST': host,
    }
    for header in headers or ():
        key, _, value = header.partition(':')
        var['HTTP_' + key.strip().upper()] = value.strip()
    var['SERVER_NAME'] = var['HTTP_HOST']
    if port:
        var['SERVER_PORT'] = str(port)
    result = ask_uwsgi(uwsgi_addr=uwsgi_addr, var=var, body=body,
                       timeout=timeout, udp=udp)
    return result


def cli(*args):
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('uwsgi_addr', nargs=1,
                        help="Remote address of uWSGI server")

    parser.add_argument('url', nargs='?', default='/',
                        help="Request URI optionally containing hostname")

    parser.add_argument('-X', '--method', default='GET',
                        help="Request method. Default: GET")

    parser.add_argument('-H', '--header', action='append', dest='headers',
                        help="Request header. It can be used multiple times")

    parser.add_argument('-d', '--data', help="Request body")

    parser.add_argument('-t', '--timeout', default=0.0, type=float,
                        help="Socket timeout")

    parser.add_argument('--udp', action='store_true',
                        help="Use UDP instead of TCP")

    args = parser.parse_args(args or sys.argv[1:])

    response = curl(uwsgi_addr=args.uwsgi_addr[0], method=args.method,
                    url=args.url, body=args.data, timeout=args.timeout,
                    headers=args.headers, udp=args.udp)
    print(response)

    status = int(response.split(' ', 2)[1])
    return not (200 <= status < 300)


if __name__ == '__main__':
    sys.exit(cli(*sys.argv[1:]))
