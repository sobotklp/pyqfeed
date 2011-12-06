import asyncore, asynchat, socket, logging, threading

import dispatcher

class Client(asynchat.async_chat, dispatcher.Dispatcher):
    '''
    Low-level IQfeed client
    '''
    DEFAULT_HOST = "127.0.0.1"
    DEFAULT_PORT = 5009 # Default Level 1 port
    
    def __init__(self, (host, port) = (DEFAULT_HOST, DEFAULT_PORT)):
        asynchat.async_chat.__init__(self)
        dispatcher.Dispatcher.__init__(self)
        self._host = host
        self._port = port
        self._connection_started = False
        self._receiver_thread = None
        self._receiver_thread_exiting = threading.Event()
        self._receiver_thread_exited = False
        
        # IQfeed terminates lines with a newline
        self.set_terminator("\n")
        
    def _connect_iqfeed(self):
        '''
        Create a socket and connect to IQfeed service
        '''
        self._connection_started = True
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect( (self._host, self._port) )
        
    def start(self):
        if self._receiver_thread:
            self.stop()
        
        self._receiver_thread_exiting.clear()
        self._connect_iqfeed()
        self._receiver_thread = threading.Thread(None, self._start_receive_loop)
        self._receiver_thread.start()

    def stop(self):
        logging.debug("Client.stop()")
        # Close the socket.
        try:
            self.close()
        except AttributeError:
            # Socket already closed.
            pass
        
        # Wait for the receiver thread to terminate.
        if self._receiver_thread != threading.currentThread(): self._receiver_thread_exiting.wait()

    def join(self):
        if self._receiver_thread:
            logging.debug("Joining %s" % self._receiver_thread.getName())
            self._receiver_thread.join()
        
    def _start_receive_loop(self):
        threading.currentThread().setName("IQFeedReceive")
        logging.debug("Thread %s starting" % threading.currentThread().getName())
        try:
            self._ibuffer = ""
            asyncore.loop()
        finally:
            logging.debug("Thread %s terminating..." % threading.currentThread().getName())
            self._receiver_thread_exiting.set()
            
    def handle_connect(self):
        self._connection_started = False
        logging.debug("Connected!")

    def handle_close(self):
        logging.debug("Disconnected.")
        self.close()

    def collect_incoming_data(self, data):
        """Buffer incoming data"""
        self._ibuffer += data

    def found_terminator(self):
        """Input reader found a new terminator (newline)"""
        self.new_message(self._ibuffer)
        self._ibuffer = ""

    def new_message(self, message):
        for listener in self._listeners.values():
            listener.on_message(message)
            
    def send(self, message):
        '''
        Send a command to the IQFeed server
        '''
        asynchat.async_chat.send(self, message + "\n")
        
