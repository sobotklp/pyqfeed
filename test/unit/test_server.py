import sys, os, threading, time, StringIO, socket, select, random
from contextlib import contextmanager

@contextmanager
def loadfixture(filename):
    fixture_file = os.path.join(os.path.dirname(__file__), "../fixture", filename)
    with open(fixture_file) as fd:
        yield fd.read()

def dummy_server(evt, port, buf, serv):
    try:
        serv.bind(('localhost', port))
        serv.listen(4)
        conn, addr = serv.accept()
    except socket.timeout:
        pass
    else:
        while True:
            r, w, e = select.select([conn], [], [], 0.1)
            if r:
                data = conn.recv(4096)
                if len(data) == 0:
                    break; # client disconnected
                buf.write(data)

                if evt.is_set():
                    break

class TestIQConnectServer:
    def __init__(self):
        self._thd = None

    def __enter__(self, *args):
        self._evt = threading.Event()
        self._buf = StringIO.StringIO()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        port = random.randint(59000, 65535)
		
        args = (self._evt, port, self._buf, sock)
        self._thd = threading.Thread(target=dummy_server, args=args)
        self._thd.start()
        time.sleep(0.2)
        return port
	
    def __exit__(self, exc_type, exc_value, traceback):
        self._evt.set()
        self._thd.join()

    def read(self, num_bytes=1):
        return self._buf.getvalue()
	
