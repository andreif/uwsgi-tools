import socket
import unittest
from uwsgi_tools.curl import cli
from tests.utils import server


class CurlTests(unittest.TestCase):
    def test_cli(self):
        with server():
            self.assertFalse(cli('127.0.0.1', 'host.name/'))

    def test_cli_nok(self):
        with server(status=300):
            self.assertTrue(cli('127.0.0.1:3030', '--timeout', '10'))

    def test_file_socket(self):
        fname = '/tmp/unix-socket'

        with server(addr=fname, params=(socket.AF_UNIX, socket.SOCK_STREAM)):
            self.assertFalse(cli(fname))

    def test_headers(self):
        with server(callback=lambda x: self.assertIn(b'localhost', x)):
            self.assertFalse(cli('127.0.0.1:3030', '-H', 'Host: localhost'))
