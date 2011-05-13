
class Dispatcher(object):
    def __init__(self):
        self._listeners = {}
        
    def set_listener(self, name, listener):
        '''
        Set a named listener for this connection.
        
        \param name name of the listener.
        \param listener the listener object
        '''
        try:
            self._listeners[name] = listener
        except:
            raise
    def del_listener(self, name):
        '''
        Remove a listener of a specific name
        
        \param name the name of the listener to remove
        '''
        del self._listeners[name]
