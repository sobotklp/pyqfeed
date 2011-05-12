import asyncore, asynchat, socket, logging, threading

class Client(asynchat.async_chat):
    '''
    Low-level IQfeed client
    '''
    DEFAULT_HOST = "127.0.0.1"
    DEFAULT_PORT = 5009 # Default Level 1 port
    
    def __init__(self, (host, port) = (DEFAULT_HOST, DEFAULT_PORT)):
        asynchat.async_chat.__init__(self)
        self._host = host
        self._port = port
        self._ibuffer = ""
        self._connection_started = False
        self._receiver_thread_exit_condition = threading.Condition()
        self._receiver_thread_exited = False
        self._listeners = {}
        
        # IQfeed terminates lines with a newline
        self.set_terminator("\n")

    def set_listener(self, name, listener):
        '''
        Set a named listener for this connection.
        
        \param name name of the listener.
        \param listener the listener object
        '''
        self._listeners[name] = listener
    
    def del_listener(self, name):
        '''
        Remove a listener of a specific name
        
        \param name the name of the listener to remove
        '''
        del self._listeners[name]
        
    def _connect_iqfeed(self):
        '''
        Create a socket and connect to IQfeed service
        '''
        self._connection_started = True
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect( (self._host, self._port) )
        
    def start(self):
        self._connect_iqfeed()
        thread = threading.Thread(None, self._start_receive_loop)
        thread.start()

    def stop(self):
        # Close the socket.
        try:
            self.close()
        except AttributeError:
            # Socket already closed.
            pass
        
        # Wait for the receiver thread to terminate.
        self._receiver_thread_exit_condition.acquire()
        if not self._receiver_thread_exited:
            self._receiver_thread_exit_condition.wait()
        self._receiver_thread_exit_condition.release()
        
    def _start_receive_loop(self):
        logging.debug( "Thread starting")
        try:
            threading.currentThread().setName("IQFeedReceive")
            asyncore.loop()
        finally:
            logging.debug("Thread %s terminating..." % threading.currentThread().getName())
            self._receiver_thread_exit_condition.acquire()
            self._receiver_thread_exited = True
            self._receiver_thread_exit_condition.notifyAll()
            self._receiver_thread_exit_condition.release()
            
    def handle_connect(self):
        self._connection_started = False
        logging.info("Connected!")

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
        