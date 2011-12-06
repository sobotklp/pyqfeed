import sys, asyncore, asynchat, socket, logging, threading, random, select

from dispatcher import Dispatcher

try:
    import queue # Python 3
except ImportError:
    import Queue as queue

class _async_comm_thread(threading.Thread):
    '''
    :py:class:`threading.Thread` for asynchronous communication with IQConnect
    '''
#    def __init__(self):
#        threading.Thread.__init__(self)
#        self.__started = threading.Event()
        
    def _start_receive_loop(self):
        threading.currentThread().setName("PyQFeed receive thread")
#        self.__started.set()
        try:
            asyncore.loop()
        finally:
            logging.debug("Thread %s terminating..." % threading.currentThread().getName())

    def run(self, *args, **kwargs):
        self._start_receive_loop()

    def wait_until_started(self):
        self.__started.wait()
        
# TODO: Allow this to be set by PyQfeed users, not have it be a singleton
_receive_thread = _async_comm_thread()

def _start_receive_loop():
    threading.currentThread().setName("PyQFeed receive %i" % random.randint(1, 1000))
    try:
        asyncore.loop()
    except select.error as e:
        pass # This happens on Windows when the thread is shutting down. Safe to ignore.
    finally:
        logging.debug("Thread %s terminating..." % threading.currentThread().getName())

class IQConnectSocketClient(asynchat.async_chat, Dispatcher):
    '''
    Low-level client to IQConnect socket interface

    In general, this class should not be instantiated directly. Instead, use one of the more specific service clients. e.g. :py:class:`pyqfeed.level1.Level1Client`
    '''
    DEFAULT_ADDR = ('127.0.0.1', 5009)

    def __init__(self, sockaddr=DEFAULT_ADDR, log=None):
        asynchat.async_chat.__init__(self)
        Dispatcher.__init__(self)
        self._host, self._port = sockaddr
        self._receiver_thread = threading.Thread(None, _start_receive_loop)
        self._close_event = threading.Event()
        self._ibuffer = ""
        self._log = log

        # IQfeed separates rows with newline
        self.set_terminator("\n")

    def _connect_iqfeed(self):
        '''
        Initiate connection to IQFeed
        '''
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self._host, self._port))
        self.set_socket(s)

        # Start listener thread if it's not already running.
        if not self._receiver_thread.is_alive():
            self._receiver_thread.start()
            #self._receiver_thread.wait_until_started()

    def connect(self):
        try:
            self._connect_iqfeed()
        except Exception, e:
            raise
        finally:
            pass

    def disconnect(self):
        try:
            self.close()
        except AttributeError:
            # Socket is already closed
            pass

    def handle_error(self):
        '''
        Called when an unhandled exception occurs
        '''
        t, v, tb = sys.exc_info()
        logging.error(t)
        self.close()

    def handle_connect(self):
        '''
        Called when connection is established
        '''
        logging.debug("Connected!")
        #self._q.put((None, None))
        
    def handle_close(self):
        logging.debug("Disconnected!")
        self.disconnect()

    def collect_incoming_data(self, data):
        '''
        Buffer new data
        '''
        self._ibuffer += data

    def found_terminator(self):
        '''
        Called when a new message has been received. See :py:class:`asynchat.async_chat`.
        '''
        self.new_message(self._ibuffer)
        self._ibuffer = ""

    def new_message(self, data):
        pass

    def send(self, message):
        '''
        Send message to IQConnect
        '''
        asynchat.async_chat.send(self, message + "\n")

    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()
        
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    c = IQConnectSocketClient()
    try:
        c.connect()
        c.send("wFXC")
        import time; time.sleep(1)
        c.disconnect()
    except Exception as e:
        import traceback; logging.debug(traceback.format_exc())
        
