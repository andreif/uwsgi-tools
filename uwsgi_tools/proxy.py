import sys
if sys.version_info[0] == 3:
    from socketserver import TCPServer
    from http.server import BaseHTTPRequestHandler
else:
    from SocketServer import TCPServer
    from BaseHTTPServer import BaseHTTPRequestHandler
from wsgiref.simple_server import WSGIRequestHandler

from .curl import ask_uwsgi
from .utils import parse_addr


class RequestHandler(WSGIRequestHandler):
    handle = BaseHTTPRequestHandler.handle

    def write(self, s):
        self.wfile.write(s.encode('utf8'))
        self.close_connection = 1

    def do(self):
        self.log_message(self.requestline.rpartition(' ')[0])

        if self.server.redirect_static:
            if any(map(self.path.startswith, ['/static/', '/media/'])):
                return self.write('HTTP/1.1 302 Found\nLocation: http://%s%s\n'
                                  % (self.server.uwsgi_host, self.path))

        setattr(self.server, 'base_environ', {})
        env = WSGIRequestHandler.get_environ(self)
        qs = env['QUERY_STRING']
        env = dict(dict({
            'REQUEST_URI': env['PATH_INFO'] + (('?' + qs) if qs else ''),
            'CONTENT_LENGTH': '',
            'DOCUMENT_ROOT': '',
            'REMOTE_PORT': str(self.client_address[1]),
        }, **env), **{
            'SERVER_ADDR': self.server.uwsgi_addr,
            'SERVER_NAME': self.server.uwsgi_host,
            'SERVER_PORT': str(self.server.uwsgi_port),
            'CONTENT_TYPE': (self.headers.get('content-type')
                             if sys.version_info[0] == 3
                             else self.headers.typeheader) or '',
            'HTTP_HOST': self.server.uwsgi_host,
        })
        env.pop('REMOTE_HOST', 0)
        env.pop('HTTP_REFERER', 0)

        cl = env['CONTENT_LENGTH']
        body = repr(self.rfile.read(int(cl))) if cl else ''

        resp = ask_uwsgi((self.server.uwsgi_addr, self.server.uwsgi_port),
                         var=env, body=body)
        self.write(resp)
        h, _, b = resp.partition('\r\n\r\n')
        print('%s\n%s' % (h, len(b)))

    do_HEAD = do_GET = do_POST = do


def serve_forever(uwsgi_addr, uwsgi_host=None, local_addr='',
                  redirect_static=True):

    uwsgi_addr, uwsgi_port = parse_addr(uwsgi_addr, 3030)
    local_addr = parse_addr(local_addr, uwsgi_port)

    print('Proxying remote uWSGI server %s:%s "%s" to local HTTP server '
          '%s:%s...' % (uwsgi_addr, uwsgi_port, (uwsgi_host or ''),
                        local_addr[0], local_addr[1]))

    TCPServer.allow_reuse_address = True
    s = TCPServer(
        server_address=local_addr,
        RequestHandlerClass=RequestHandler,
    )
    s.uwsgi_addr = uwsgi_addr
    s.uwsgi_port = uwsgi_port
    s.uwsgi_host = uwsgi_host or uwsgi_addr
    s.redirect_static = redirect_static
    try:
        s.serve_forever()
    except KeyboardInterrupt:
        s.shutdown()
        s.server_close()
        print(' Bye.')


def cli(*args):
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('uwsgi_addr', nargs=1,
                        help='Remote address of uWSGI server')
    parser.add_argument('-n', '--http-host',
                        help='HTTP_HOST header for uWSGI server')
    parser.add_argument('-l', '--local-addr', default='127.0.0.1',
                        help='Local address of HTTP server')
    parser.add_argument('-s', '--redirect-static', action='store_true',
                        default=False, help='Redirect static requests to host')

    args = parser.parse_args(args or sys.argv[1:])
    serve_forever(
        uwsgi_addr=args.uwsgi_addr[0],
        uwsgi_host=args.http_host,
        local_addr=args.local_addr,
        redirect_static=args.redirect_static,
    )


if __name__ == '__main__':
    cli()
