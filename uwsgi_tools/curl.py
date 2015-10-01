import socket
from .utils import pack_uwsgi_vars, parse_addr, get_host_from_url


def ask_uwsgi(addr_and_port, var, body=''):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(parse_addr(addr_and_port))
    s.send(pack_uwsgi_vars(var) + body.encode('utf8'))
    response = []
    while 1:
        data = s.recv(4096)
        if not data:
            break
        response.append(data)
    s.close()
    return b''.join(response).decode('utf8')


def curl(addr_and_port, url):
    host, uri = get_host_from_url(url)
    path, _, qs = uri.partition('?')
    host = host or parse_addr(addr_and_port)[0]
    var = {
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'REQUEST_METHOD': 'GET',
        'PATH_INFO': path,
        'REQUEST_URI': uri,
        'QUERY_STRING': qs,
        'SERVER_NAME': host,
        'HTTP_HOST': host,
    }
    return ask_uwsgi(addr_and_port, var)


def cli(*args):
    import argparse
    import sys

    parser = argparse.ArgumentParser()

    parser.add_argument('uwsgi_addr', nargs=1,
                        help='Remote address of uWSGI server')

    parser.add_argument('url', nargs='?', default='/',
                        help='Request URI optionally containing hostname')

    args = parser.parse_args(args or sys.argv[1:])
    print(curl(args.uwsgi_addr[0], args.url))


if __name__ == '__main__':
    cli()
