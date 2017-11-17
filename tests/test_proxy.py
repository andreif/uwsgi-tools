import unittest
from uwsgi_tools import proxy
from tests.compat import mock
from tests.utils import server


class ProxyTests(unittest.TestCase):
    def setUp(self):
        self.srv_mock = mock.Mock(uwsgi_addr='127.0.0.1', uwsgi_port=3030,
                                  uwsgi_host='uwsgi.host')

    @mock.patch('uwsgi_tools.proxy.TCPServer')
    def test_cli(self, srv):
        srv.return_value.serve_forever.side_effect = [KeyboardInterrupt]
        proxy.cli('127.0.0.1:3030', '-l', '8080')

    def test_handler(self):
        req = mock.Mock(**{'makefile.return_value.readline.side_effect': [
            b'GET / HTTP/1.1\r\n',
            b'\r\n',
        ]})
        with server():
            proxy.RequestHandler(request=req, client_address=['client', 0],
                                 server=self.srv_mock)

    def test_handler_static(self):
        req = mock.Mock(**{'makefile.return_value.readline.side_effect': [
            b'GET /static/img HTTP/1.1\r\n',
            b'\r\n',
        ]})
        self.srv_mock.redirect_static = True
        proxy.RequestHandler(request=req, client_address=['client', 0],
                             server=self.srv_mock)
