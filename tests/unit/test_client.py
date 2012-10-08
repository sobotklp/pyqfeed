import unittest, socket
from test_server import TestIQConnectServer

from pyqfeed.client import IQConnectSocketClient

class TestIQConnectSocketClient(unittest.TestCase):
    def setUp(self):
        self.test_server = TestIQConnectServer()

    def test_cantconnect(self):
        client = IQConnectSocketClient( ('localhost', 0) )
        self.assertRaises(socket.error, client.connect)

    def test_connect(self):
        with self.test_server as port:
            client = IQConnectSocketClient( ('localhost', port) )
            client.connect()
            client.disconnect()

            
    def test_send(self):
        with self.test_server as port:
            client = IQConnectSocketClient( ('localhost', port) )
            client.connect()
            client.send("Test message!")
            client.disconnect()
        self.assertEquals(self.test_server.read(), "Test message!\n") # Newline added by PyQFeed
 
    def test_connect_with_context_manager(self):
        with self.test_server as port:
            client = IQConnectSocketClient( ('localhost', port) )
            with client as iqfeed:
                iqfeed.send("test_connect_with_context_manager")
        self.assertEquals(self.test_server.read(), "test_connect_with_context_manager\n") # Newline added by PyQFeed
                
