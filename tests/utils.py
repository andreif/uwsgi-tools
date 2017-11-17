import os
import socket
import time
import threading
from contextlib import contextmanager
from tests.compat import str2bytes


@contextmanager
def server(addr=('127.0.0.1', 3030), params=(), status=200, callback=None):
    if isinstance(addr, str) and addr.startswith('/tmp/'):
        if os.path.exists(addr):
            os.unlink(addr)

    def target():
        s = socket.socket(*params)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(addr)
        s.listen(1)
        conn, _ = s.accept()
        # with conn:
        request = conn.recv(2048)
        if callback:
            callback(request)
        conn.send(str2bytes('HTTP/1.1 %s' % status))
        s.close()
    th = threading.Thread(target=target)
    th.start()
    time.sleep(0.001)
    yield
    th.join()
