class Listener(object):
    def on_error(self, message):
        pass
    
    def on_data_start(self, symbol):
        pass
    
    def on_data_finished(self):
        pass
    
    def on_message(self, message, **kwargs):
        """
        Called by the IQFeed connection when there is a new message to process
        """
        pass
    
    